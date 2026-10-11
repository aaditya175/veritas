"""
Veritas Text Generator: Google Gemini API Backend
Leverages Gemini 1.5 Flash free tier for conditional synthetic text generation.
"""
import os
import json
import httpx
from typing import List, Dict, Any, Optional
from app.core.base_generator import BaseTextGenerator, Modality


class GeminiTextGenerator(BaseTextGenerator):
    name = "gemini_flash"
    display_name = "Google Gemini (1.5 Flash - Free Tier)"
    modality = Modality.TEXT
    description = "Google Gemini 1.5 Flash text generator capturing deep context, semantic style, and label conditioning."

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    def fit(self, data: Any, **kwargs) -> Any:
        return self

    def sample(self, n: int, **kwargs) -> Any:
        return self.generate([], sample_count=n, **kwargs)

    def generate(
        self,
        corpus_texts: List[str],
        sample_count: int = 5,
        bias_category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        api_key = kwargs.get("api_key") or self.api_key or os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("Gemini API key is required. Please set it in Settings or the generate request.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        examples_str = "\n".join([f"- {t}" for t in corpus_texts[:6]])
        category_instruction = f"Bias synthetic examples towards category/topic: '{bias_category}'." if bias_category else "Reflect the natural variety of topics and sentiments in the examples."

        prompt_text = f"""You are Veritas Text Synthesizer.
Analyze the following sample texts from a user corpus:
{examples_str}

Requirement:
Generate exactly {sample_count} realistic synthetic text samples that faithfully match the length, vocabulary style, and tone of the originals.
{category_instruction}

Respond with a raw JSON array of objects only:
[{{"text": "example text...", "category": "category name..."}}]
Do not include markdown code block syntax."""

        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1500
            }
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API returned error {resp.status_code}: {resp.text}")
            
            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Clean JSON
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        try:
            parsed = json.loads(raw_text)
            if isinstance(parsed, list):
                return parsed[:sample_count]
            return [{"text": raw_text, "category": bias_category or "Synthetic"}]
        except Exception:
            lines = [l.strip().lstrip('0123456789.-" ') for l in raw_text.split('\n') if l.strip()]
            return [{"text": l, "category": bias_category or "Synthetic"} for l in lines[:sample_count]]
