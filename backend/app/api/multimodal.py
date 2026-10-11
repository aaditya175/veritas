"""
Veritas Multimodal API Endpoints (Future Scope Architecture)
Exposes architectural blueprints and plugin schemas for Image and Video generators.
"""
from fastapi import APIRouter
from app.core.registry import GeneratorRegistry
from app.multimodal.image_generator import CausalVAEImageGenerator
from app.multimodal.video_generator import CausalVideoDiffusionGenerator

router = APIRouter(prefix="/api/multimodal", tags=["Multimodal Architecture"])


@router.get("/catalog")
def get_multimodal_catalog():
    return GeneratorRegistry.get_modalities_catalog()


@router.get("/image/blueprint")
def get_image_blueprint():
    img_gen = CausalVAEImageGenerator()
    return {
        "status": "coming_soon",
        "phase": "Phase 4 Multimodal Extension",
        "model_name": img_gen.name,
        "display_name": img_gen.display_name,
        "description": img_gen.description,
        "blueprint": img_gen.get_architecture_blueprint()
    }


@router.get("/video/blueprint")
def get_video_blueprint():
    vid_gen = CausalVideoDiffusionGenerator()
    return {
        "status": "coming_soon",
        "phase": "Phase 5 Multimodal Extension",
        "model_name": vid_gen.name,
        "display_name": vid_gen.display_name,
        "description": vid_gen.description,
        "blueprint": vid_gen.get_architecture_blueprint()
    }
