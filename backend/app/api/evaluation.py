"""
Veritas Comparative Evaluation API Endpoints
Aggregates and formats benchmark comparisons across generative backends.
"""
import json
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, DatasetModel, GenerationJobModel

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])


@router.get("/compare/{dataset_id}")
def compare_models(dataset_id: str, db: Session = Depends(get_db)):
    """
    Returns comparative scorecard comparing all generative backends on the dataset.
    """
    jobs = db.query(GenerationJobModel).filter(GenerationJobModel.dataset_id == dataset_id).order_by(GenerationJobModel.created_at.desc()).all()
    if not jobs:
        return {"models": [], "summary": "No generation runs found for this dataset yet."}

    # Group latest run per model
    latest_by_model: Dict[str, GenerationJobModel] = {}
    for job in jobs:
        if job.model_name not in latest_by_model:
            latest_by_model[job.model_name] = job

    comparison_cards = []
    for m_name, j in latest_by_model.items():
        metrics = json.loads(j.metrics_json) if j.metrics_json else {}
        comparison_cards.append({
            "job_id": j.id,
            "model_name": j.model_name,
            "display_name": j.display_name,
            "fidelity": metrics.get("fidelity", {}).get("overall", 0.0),
            "utility": metrics.get("utility", {}).get("score", 0.0),
            "privacy": metrics.get("privacy", {}).get("score", 0.0),
            "fairness": metrics.get("fairness", {}).get("score", 0.0),
            "training_time": metrics.get("performance", {}).get("training_time_seconds", 0.0),
            "num_samples": j.num_samples,
            "created_at": j.created_at.isoformat() if j.created_at else None
        })

    # Find top performers
    best_fidelity = max(comparison_cards, key=lambda x: x["fidelity"], default=None)
    best_utility = max(comparison_cards, key=lambda x: x["utility"], default=None)
    best_privacy = max(comparison_cards, key=lambda x: x["privacy"], default=None)

    return {
        "models": comparison_cards,
        "highlights": {
            "best_fidelity": best_fidelity["display_name"] if best_fidelity else None,
            "best_utility": best_utility["display_name"] if best_utility else None,
            "best_privacy": best_privacy["display_name"] if best_privacy else None
        }
    }
