"""
Veritas Platform Settings API Endpoints
Manages optional API keys (Groq, Gemini) and system configuration.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db, SettingModel

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("")
def get_settings(db: Session = Depends(get_db)):
    groq_set = db.query(SettingModel).filter(SettingModel.key == "groq_api_key").first()
    gemini_set = db.query(SettingModel).filter(SettingModel.key == "gemini_api_key").first()

    has_groq = bool(groq_set and groq_set.value)
    has_gemini = bool(gemini_set and gemini_set.value)

    return {
        "has_groq_api_key": has_groq,
        "groq_masked": (groq_set.value[:4] + "..." + groq_set.value[-4:]) if has_groq and len(groq_set.value) > 8 else ("Configured" if has_groq else ""),
        "has_gemini_api_key": has_gemini,
        "gemini_masked": (gemini_set.value[:4] + "..." + gemini_set.value[-4:]) if has_gemini and len(gemini_set.value) > 8 else ("Configured" if has_gemini else ""),
        "environment": "local"
    }


@router.post("")
def save_settings(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    groq_key = payload.get("groq_api_key")
    gemini_key = payload.get("gemini_api_key")

    if groq_key is not None:
        rec = db.query(SettingModel).filter(SettingModel.key == "groq_api_key").first()
        if not rec:
            rec = SettingModel(key="groq_api_key", value=groq_key.strip())
            db.add(rec)
        else:
            rec.value = groq_key.strip()

    if gemini_key is not None:
        rec = db.query(SettingModel).filter(SettingModel.key == "gemini_api_key").first()
        if not rec:
            rec = SettingModel(key="gemini_api_key", value=gemini_key.strip())
            db.add(rec)
        else:
            rec.value = gemini_key.strip()

    db.commit()
    return {"status": "success", "message": "Settings updated successfully"}
