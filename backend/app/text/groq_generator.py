"""
Veritas Text Generator: Groq API Backend
Fast inference on open LLMs (Llama 3.1 8B) via Groq's free tier.
"""
import os
import json
from typing import List, Dict, Any, Optional
from app.core.base_generator import BaseTextGenerator, Modality

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class GroqTextGenerator(BaseTextGenerator):
    name = "groq_llama3"
    display_name = "Groq (Llama 3.1 - Free Tier)"
    modality = Modality.TEXT
    description = "Ultra-fast text generation powered by Llama 3.1 8B on Groq LPUs with style conditioning."

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.is_available = GROQ_AVAILABLE

    def fit(self, data: Any, **kwargs) -> Any:
        # LLM text generators are in-context learners; fit validates configuration
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
        api_key = kwargs.get("api_key") or self.api_key or os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("Groq API key is required. Please provide it in Settings or the generate request.")

        client = Groq(api_key=api_key)
        
        # Build prompt from corpus samples and metadata
        examples_str = "\n".join([f"- {t}" for t in corpus_texts[:6]])
        category_instruction = f"Bias the generated samples towards category/topic: '{bias_category}'." if bias_category else "Reflect the natural variety of topics and sentiments in the examples."

        system_prompt = (
            "You are Veritas Text Synthesizer, an expert causal and probabilistic synthetic data engine. "
            "Your task is to generate realistic synthetic text examples matching the stylistic tone, "
            "vocabulary level, sentence structure, and distribution of the provided reference corpus. "
            "Output ONLY valid JSON formatted as an array of objects: "
            '[{"text": "...", "category": "..."}] with no extra text or markdown codeblocks.'
        )

        user_prompt = f"""Reference Examples from user corpus:
{examples_str}

Requirement:
1. Generate exactly {sample_count} new, distinct synthetic items.
2. {category_instruction}
3. Maintain realistic variability, vocabulary tone, and similar document length.

Return JSON array only:"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75,
            max_tokens=1500
        )

        raw_content = response.choices[0].message.content.strip()
        # Clean markdown wrappers if present
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        if raw_content.startswith("```"):
            raw_content = raw_content[3:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
        raw_content = raw_content.strip()

        try:
            parsed = json.loads(raw_content)
            if isinstance(parsed, list):
                return parsed[:sample_count]
            return [{"text": raw_content, "category": bias_category or "Synthetic"}]
        except Exception:
            # Fallback parsing line by line
            lines = [l.strip().lstrip('0123456789.-" ') for l in raw_content.split('\n') if l.strip()]
            return [{"text": l, "category": bias_category or "Synthetic"} for l in lines[:sample_count]]
