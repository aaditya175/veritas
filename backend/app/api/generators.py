"""
Veritas Generator Execution API Endpoints
Runs tabular synthetic data generation across registered backends, evaluates scorecards,
and stores reproducible run metadata.
"""
import os
import time
import uuid
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db, DatasetModel, GenerationJobModel
from app.core.registry import GeneratorRegistry
from app.tabular.evaluator import TabularEvaluator
from app.tabular.explainer import TabularExplainer

router = APIRouter(prefix="/api/generators", tags=["Generators"])

OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)


@router.get("")
def list_generators(modality: Optional[str] = None):
    return GeneratorRegistry.list_generators(modality=modality)


@router.get("/catalog")
def get_catalog():
    return GeneratorRegistry.get_modalities_catalog()


@router.post("/tabular/generate")
def generate_tabular(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """
    Fits selected tabular model and generates synthetic samples.
    Computes fidelity, utility, privacy scorecards and SHAP divergence explanations.
    """
    dataset_id = payload.get("dataset_id")
    model_name = payload.get("model_name", "causal_scm")
    num_samples = int(payload.get("num_samples", 150))

    d = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")

    generator = GeneratorRegistry.get("tabular", model_name)
    if not generator:
        raise HTTPException(status_code=400, detail=f"Generator '{model_name}' not found in registry.")

    df_real = pd.read_csv(d.file_path)
    causal_graph = json.loads(d.causal_graph) if d.causal_graph else None

    # Measure fit & sample time
    start_time = time.time()
    try:
        generator.fit(df_real, causal_graph=causal_graph)
        df_syn = generator.sample(n=num_samples)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed on backend '{model_name}': {str(e)}")
    
    elapsed_time = time.time() - start_time

    # Save synthetic CSV to disk
    job_id = str(uuid.uuid4())
    syn_filename = f"syn_{model_name}_{job_id[:8]}.csv"
    syn_filepath = os.path.join(OUTPUTS_DIR, syn_filename)
    df_syn.to_csv(syn_filepath, index=False)

    # Compute Evaluation Scorecard (Fidelity, Utility, Privacy, Fairness)
    metrics = TabularEvaluator.evaluate(df_real, df_syn, train_time_sec=elapsed_time)

    # Compute SHAP Divergence Explanations
    shap_report = TabularExplainer.explain_divergence(df_real, df_syn)

    # Store experiment run in database
    job_record = GenerationJobModel(
        id=job_id,
        dataset_id=dataset_id,
        model_name=model_name,
        display_name=generator.display_name,
        status="completed",
        num_samples=num_samples,
        output_path=syn_filepath,
        metrics_json=json.dumps(metrics),
        shap_json=json.dumps(shap_report)
    )
    db.add(job_record)
    db.commit()

    return {
        "job_id": job_id,
        "dataset_id": dataset_id,
        "model_name": model_name,
        "display_name": generator.display_name,
        "status": "completed",
        "num_samples": num_samples,
        "elapsed_seconds": round(elapsed_time, 2),
        "metrics": metrics,
        "shap_explainability": shap_report,
        "preview_rows": df_syn.head(15).to_dict(orient="records")
    }


@router.get("/jobs/dataset/{dataset_id}")
def get_jobs_for_dataset(dataset_id: str, db: Session = Depends(get_db)):
    jobs = db.query(GenerationJobModel).filter(GenerationJobModel.dataset_id == dataset_id).order_by(GenerationJobModel.created_at.desc()).all()
    return [{
        "id": j.id,
        "model_name": j.model_name,
        "display_name": j.display_name,
        "num_samples": j.num_samples,
        "created_at": j.created_at.isoformat() if j.created_at else None,
        "metrics": json.loads(j.metrics_json),
        "shap": json.loads(j.shap_json)
    } for j in jobs]


@router.get("/jobs/{job_id}")
def get_job_detail(job_id: str, db: Session = Depends(get_db)):
    j = db.query(GenerationJobModel).filter(GenerationJobModel.id == job_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Generation job not found")

    df_syn = pd.read_csv(j.output_path) if os.path.exists(j.output_path) else pd.DataFrame()

    return {
        "id": j.id,
        "dataset_id": j.dataset_id,
        "model_name": j.model_name,
        "display_name": j.display_name,
        "num_samples": j.num_samples,
        "created_at": j.created_at.isoformat() if j.created_at else None,
        "metrics": json.loads(j.metrics_json),
        "shap": json.loads(j.shap_json),
        "preview_rows": df_syn.head(20).to_dict(orient="records")
    }


@router.get("/jobs/{job_id}/download")
def download_synthetic_csv(job_id: str, db: Session = Depends(get_db)):
    j = db.query(GenerationJobModel).filter(GenerationJobModel.id == job_id).first()
    if not j or not os.path.exists(j.output_path):
        raise HTTPException(status_code=404, detail="Synthetic CSV file not found")
    
    filename = f"synthetic_{j.model_name}_{job_id[:8]}.csv"
    return FileResponse(j.output_path, media_type="text/csv", filename=filename)
