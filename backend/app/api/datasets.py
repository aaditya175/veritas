"""
Veritas Dataset API Endpoints
Handles CSV dataset upload, automated profiling, and preloaded sample datasets.
"""
import os
import uuid
import json
import shutil
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, DatasetModel
from app.tabular.causal_generator import CausalStructuralGenerator

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")


def profile_dataframe(df: pd.DataFrame) -> dict:
    columns_info = []
    candidate_sensitive = ["age", "gender", "sex", "race", "ethnicity", "religion", "marital_status", "nationality"]

    for col in df.columns:
        is_num = pd.api.types.is_numeric_dtype(df[col])
        null_count = int(df[col].isnull().sum())
        unique_count = int(df[col].nunique())
        is_sensitive = any(s in col.lower() for s in candidate_sensitive)

        col_dict = {
            "name": col,
            "type": "numeric" if is_num else "categorical",
            "null_count": null_count,
            "null_pct": round(float(null_count / max(len(df), 1) * 100), 1),
            "unique_count": unique_count,
            "is_sensitive": is_sensitive
        }

        if is_num:
            clean = df[col].dropna()
            col_dict.update({
                "mean": round(float(clean.mean()), 2) if not clean.empty else 0,
                "std": round(float(clean.std()), 2) if not clean.empty else 0,
                "min": round(float(clean.min()), 2) if not clean.empty else 0,
                "max": round(float(clean.max()), 2) if not clean.empty else 0,
                "median": round(float(clean.median()), 2) if not clean.empty else 0
            })
        else:
            top_cats = df[col].value_counts().head(5).to_dict()
            col_dict["top_categories"] = {str(k): int(v) for k, v in top_cats.items()}

        columns_info.append(col_dict)

    return {
        "row_count": len(df),
        "col_count": len(df.columns),
        "columns": columns_info,
        "memory_mb": round(float(df.memory_usage(deep=True).sum() / (1024 * 1024)), 2)
    }


@router.get("")
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(DatasetModel).order_by(DatasetModel.created_at.desc()).all()
    return [{
        "id": d.id,
        "name": d.name,
        "row_count": d.row_count,
        "col_count": d.col_count,
        "created_at": d.created_at.isoformat() if d.created_at else None
    } for d in datasets]


@router.get("/{dataset_id}")
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    d = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    if not os.path.exists(d.file_path):
        raise HTTPException(status_code=404, detail="Dataset file missing on disk")

    df = pd.read_csv(d.file_path)
    preview = df.head(15).to_dict(orient="records")

    return {
        "id": d.id,
        "name": d.name,
        "row_count": d.row_count,
        "col_count": d.col_count,
        "created_at": d.created_at.isoformat() if d.created_at else None,
        "profile": json.loads(d.profile_data),
        "causal_graph": json.loads(d.causal_graph),
        "preview_rows": preview
    }


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    dataset_id = str(uuid.uuid4())
    filename = file.filename or f"dataset_{dataset_id[:8]}.csv"
    dest_path = os.path.join(UPLOAD_DIR, f"{dataset_id}_{filename}")

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(dest_path)
    profile = profile_dataframe(df)

    # Initial causal discovery
    cg = CausalStructuralGenerator()
    discovered_graph = cg.discover_graph(df)

    dataset_record = DatasetModel(
        id=dataset_id,
        name=filename,
        row_count=len(df),
        col_count=len(df.columns),
        file_path=dest_path,
        profile_data=json.dumps(profile),
        causal_graph=json.dumps(discovered_graph)
    )
    db.add(dataset_record)
    db.commit()

    return {
        "id": dataset_id,
        "name": filename,
        "row_count": len(df),
        "col_count": len(df.columns),
        "profile": profile,
        "causal_graph": discovered_graph
    }


@router.post("/load-default")
def load_default_dataset(db: Session = Depends(get_db)):
    default_csv = os.path.join(SAMPLE_DIR, "employee_data.csv")
    if not os.path.exists(default_csv):
        raise HTTPException(status_code=404, detail="Default sample data not found")

    dataset_id = "default_employee_data"
    existing = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if existing:
        return {
            "id": existing.id,
            "name": existing.name,
            "row_count": existing.row_count,
            "col_count": existing.col_count,
            "profile": json.loads(existing.profile_data),
            "causal_graph": json.loads(existing.causal_graph)
        }

    df = pd.read_csv(default_csv)
    profile = profile_dataframe(df)
    cg = CausalStructuralGenerator()
    discovered_graph = cg.discover_graph(df)

    record = DatasetModel(
        id=dataset_id,
        name="employee_data.csv",
        row_count=len(df),
        col_count=len(df.columns),
        file_path=default_csv,
        profile_data=json.dumps(profile),
        causal_graph=json.dumps(discovered_graph)
    )
    db.add(record)
    db.commit()

    return {
        "id": dataset_id,
        "name": "employee_data.csv",
        "row_count": len(df),
        "col_count": len(df.columns),
        "profile": profile,
        "causal_graph": discovered_graph
    }
