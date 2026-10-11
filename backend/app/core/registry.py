"""
Veritas Generator Registry
Central registry decoupling backend algorithms from API routers and UI rendering.
Enables plug-and-play addition of new models across Tabular, Text, Image, and Video.
"""
from typing import Dict, List, Optional, Type
from app.core.base_generator import BaseGenerator, Modality


class GeneratorRegistry:
    _registry: Dict[str, Dict[str, BaseGenerator]] = {
        Modality.TABULAR.value: {},
        Modality.TEXT.value: {},
        Modality.IMAGE.value: {},
        Modality.VIDEO.value: {},
    }

    @classmethod
    def register(cls, generator_instance: BaseGenerator) -> None:
        """Register a instantiated generator plugin."""
        modality = generator_instance.modality.value
        if modality not in cls._registry:
            cls._registry[modality] = {}
        cls._registry[modality][generator_instance.name] = generator_instance

    @classmethod
    def get(cls, modality: str, name: str) -> Optional[BaseGenerator]:
        """Fetch generator by modality and model name."""
        return cls._registry.get(modality, {}).get(name)

    @classmethod
    def list_generators(cls, modality: Optional[str] = None) -> List[Dict]:
        """List metadata for registered generators, optionally filtered by modality."""
        results = []
        if modality:
            generators = cls._registry.get(modality, {}).values()
            return [g.get_info() for g in generators]
        
        for m_key, group in cls._registry.items():
            for g in group.values():
                results.append(g.get_info())
        return results

    @classmethod
    def get_modalities_catalog(cls) -> Dict[str, Dict]:
        """Return full platform modalities catalog with readiness flags."""
        return {
            "tabular": {
                "label": "Tabular / CSV",
                "status": "active",
                "description": "Deep generative baselines and Causal SCM with DAG editing & counterfactuals.",
                "models": [g.get_info() for g in cls._registry.get(Modality.TABULAR.value, {}).values()]
            },
            "text": {
                "label": "Text Corpus",
                "status": "active",
                "description": "Style-conditioned LLM synthesis with vocabulary & length distribution metrics.",
                "models": [g.get_info() for g in cls._registry.get(Modality.TEXT.value, {}).values()]
            },
            "image": {
                "label": "Image Synthesis",
                "status": "coming_soon",
                "description": "Causal Latent Factor manipulation (CausalVAE) and disentangled representation learning.",
                "models": [g.get_info() for g in cls._registry.get(Modality.IMAGE.value, {}).values()]
            },
            "video": {
                "label": "Video Synthesis",
                "status": "coming_soon",
                "description": "Spatiotemporal Causal Diffusion for physical dynamics and trajectory intervention.",
                "models": [g.get_info() for g in cls._registry.get(Modality.VIDEO.value, {}).values()]
            }
        }
