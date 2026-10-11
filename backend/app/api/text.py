"""
Veritas Text Generation API Endpoints
Handles corpus analysis, prompt synthesis, multi-backend LLM inference, and explainability.
"""
import os
import json
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db, TextJobModel, SettingModel
from app.core.registry import GeneratorRegistry
from app.text.corpus_analyzer import TextCorpusAnalyzer

router = APIRouter(prefix="/api/text", tags=["Text Generation"])

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")


@router.post("/analyze")
def analyze_corpus(payload: Dict[str, Any] = Body(...)):
    """Profiles text records for length distribution, vocabulary, tone, and category mix."""
    records = payload.get("records", [])
    if not records:
        raise HTTPException(status_code=400, detail="No text records provided.")
    
    profile = TextCorpusAnalyzer.profile_corpus(records)
    return profile


@router.post("/generate")
def generate_text(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """
    Synthesizes new text samples matching the analyzed style, length, and label distribution.
    Computes text explainability (vocabulary Jaccard overlap, length alignment).
    """
    records = payload.get("records", [])
    model_name = payload.get("model_name", "local_synthesizer")
    sample_count = int(payload.get("sample_count", 5))
    bias_category = payload.get("bias_category")
    api_key = payload.get("api_key")

    if not records:
        # Load sample fallback
        sample_path = os.path.join(SAMPLE_DIR, "customer_feedback.json")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                records = json.load(f)

    corpus_texts = [str(r.get("text", "")) for r in records if str(r.get("text", ""))]
    
    # Retrieve API key from settings if not supplied in request
    if not api_key:
        if "groq" in model_name:
            setting = db.query(SettingModel).filter(SettingModel.key == "groq_api_key").first()
            if setting and setting.value:
                api_key = setting.value
        elif "gemini" in model_name:
            setting = db.query(SettingModel).filter(SettingModel.key == "gemini_api_key").first()
            if setting and setting.value:
                api_key = setting.value

    generator = GeneratorRegistry.get("text", model_name)
    if not generator:
        raise HTTPException(status_code=400, detail=f"Text generator '{model_name}' not found.")

    try:
        synthetic_items = generator.generate(
            corpus_texts=corpus_texts,
            sample_count=sample_count,
            bias_category=bias_category,
            api_key=api_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text generation error: {str(e)}")

    # Compute Explainability & Distribution Alignment
    syn_texts = [str(s.get("text", "")) for s in synthetic_items]
    eval_metrics = TextCorpusAnalyzer.compare_real_and_synthetic(corpus_texts, syn_texts)

    # Store run
    job_id = str(uuid.uuid4())
    job_record = TextJobModel(
        id=job_id,
        model_name=model_name,
        sample_count=sample_count,
        bias_category=bias_category or "None",
        results_json=json.dumps(synthetic_items),
        evaluation_json=json.dumps(eval_metrics)
    )
    db.add(job_record)
    db.commit()

    return {
        "job_id": job_id,
        "model_name": model_name,
        "display_name": generator.display_name,
        "sample_count": len(synthetic_items),
        "results": synthetic_items,
        "explainability": eval_metrics
    }


@router.post("/load-default")
def load_default_text():
    sample_path = os.path.join(SAMPLE_DIR, "customer_feedback.json")
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Default sample text data not found")

    with open(sample_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    profile = TextCorpusAnalyzer.profile_corpus(records)
    return {
        "records": records,
        "profile": profile
    }
