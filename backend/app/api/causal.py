"""
Veritas Causal Graph & Counterfactual API Endpoints
Enables interactive human-in-the-loop DAG editing and Pearl's 3-step counterfactual exploration.
"""
import json
import pandas as pd
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db, DatasetModel
from app.tabular.causal_generator import CausalStructuralGenerator

router = APIRouter(prefix="/api/causal", tags=["Causal Engine"])

# Cache fitted causal models per dataset & graph version for instant counterfactual responses
_CACHED_CAUSAL_MODELS: Dict[str, CausalStructuralGenerator] = {}


@router.get("/{dataset_id}/graph")
def get_causal_graph(dataset_id: str, db: Session = Depends(get_db)):
    d = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    graph = json.loads(d.causal_graph) if d.causal_graph else {}
    return graph


@router.post("/{dataset_id}/graph")
def update_causal_graph(dataset_id: str, graph_data: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """
    Saves human-in-the-loop DAG corrections (added, removed, or reversed edges).
    """
    d = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")

    d.causal_graph = json.dumps(graph_data)
    db.commit()

    # Invalidate cached model for this dataset so next run refits with updated DAG
    if dataset_id in _CACHED_CAUSAL_MODELS:
        del _CACHED_CAUSAL_MODELS[dataset_id]

    return {"status": "success", "message": "Causal DAG updated successfully", "graph": graph_data}


@router.post("/{dataset_id}/counterfactual")
def run_counterfactual(
    dataset_id: str,
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """
    Executes Pearl's 3-step counterfactual query:
    1. Abduction: infer individual's latent noise epsilon from factual row
    2. Action: intervene on target feature (do(X = v))
    3. Prediction: recompute downstream causal descendants in topological order
    """
    d = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")

    row = payload.get("row")
    target_feature = payload.get("target_feature")
    new_value = payload.get("new_value")

    if not row or not target_feature:
        raise HTTPException(status_code=400, detail="Both 'row' and 'target_feature' are required.")

    df = pd.read_csv(d.file_path)
    causal_graph = json.loads(d.causal_graph) if d.causal_graph else None

    # Get or fit causal structural model
    if dataset_id not in _CACHED_CAUSAL_MODELS:
        model = CausalStructuralGenerator()
        model.fit(df, causal_graph=causal_graph)
        _CACHED_CAUSAL_MODELS[dataset_id] = model
    else:
        model = _CACHED_CAUSAL_MODELS[dataset_id]

    try:
        cf_result = model.intervene(row, target_feature, new_value)
        return cf_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Counterfactual computation failed: {str(e)}")
