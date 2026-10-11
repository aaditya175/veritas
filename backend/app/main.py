"""
Veritas Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import init_db
from app.core.setup_registry import register_all_generators
from app.api import datasets, causal, generators, evaluation, explainability, text, multimodal, settings

app = FastAPI(
    title="Veritas API — Causal & Explainable Synthetic Data Platform",
    description="Full-stack platform integrating deep generative models, causal discovery, ancestral sampling, counterfactual exploration, and XAI diagnostics.",
    version="1.0.0"
)

# Enable CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount outputs directory for file downloads
outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(outputs_dir, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=outputs_dir), name="outputs")

# Include Routers
app.include_router(datasets.router)
app.include_router(causal.router)
app.include_router(generators.router)
app.include_router(evaluation.router)
app.include_router(explainability.router)
app.include_router(text.router)
app.include_router(multimodal.router)
app.include_router(settings.router)


@app.on_event("startup")
def on_startup():
    init_db()
    register_all_generators()
    print("Veritas Backend Initialized: SQLite DB and Generator Registry active.")


@app.get("/health")
def health_check():
    return {"status": "ok", "platform": "Veritas", "version": "1.0.0"}


@app.get("/api/info")
def platform_info():
    return {
        "name": "Veritas",
        "tagline": "Causally-Grounded, Explainable Synthetic Data Platform",
        "version": "1.0.0",
        "supported_modalities": ["tabular", "text"],
        "future_modalities": ["image", "video"]
    }
