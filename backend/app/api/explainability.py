"""
Veritas Explainability API Endpoints
Returns SHAP feature importance, C2ST discriminator metrics, and causal explanation diagnostics.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, GenerationJobModel

router = APIRouter(prefix="/api/explainability", tags=["Explainability"])


@router.get("/{job_id}")
def get_explainability_report(job_id: str, db: Session = Depends(get_db)):
    job = db.query(GenerationJobModel).filter(GenerationJobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Generation job not found")

    shap_data = json.loads(job.shap_json) if job.shap_json else {}
    metrics_data = json.loads(job.metrics_json) if job.metrics_json else {}

    return {
        "job_id": job.id,
        "model_name": job.model_name,
        "display_name": job.display_name,
        "c2st_discriminator_accuracy": shap_data.get("c2st_discriminator_accuracy", 0.5),
        "fidelity_verdict": shap_data.get("fidelity_verdict", "Evaluation completed"),
        "feature_attributions": shap_data.get("feature_attributions", []),
        "top_divergence_insights": shap_data.get("top_divergence_insights", []),
        "fidelity_breakdown": metrics_data.get("fidelity", {}).get("column_breakdown", {})
    }
