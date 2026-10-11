"""
Veritas Generator Registration Initialization
Populates the central registry with all generative models across all modalities.
"""
from app.core.registry import GeneratorRegistry
from app.tabular.copula_generator import GaussianCopulaGenerator
from app.tabular.ctgan_generator import CTGANGenerator
from app.tabular.tvae_generator import TVAEGenerator
from app.tabular.causal_generator import CausalStructuralGenerator
from app.text.local_generator import LocalStyleTextGenerator
from app.text.groq_generator import GroqTextGenerator
from app.text.gemini_generator import GeminiTextGenerator
from app.multimodal.image_generator import CausalVAEImageGenerator
from app.multimodal.video_generator import CausalVideoDiffusionGenerator


def register_all_generators():
    # Tabular Generators
    GeneratorRegistry.register(CausalStructuralGenerator())
    GeneratorRegistry.register(GaussianCopulaGenerator())
    GeneratorRegistry.register(CTGANGenerator())
    GeneratorRegistry.register(TVAEGenerator())

    # Text Generators
    GeneratorRegistry.register(LocalStyleTextGenerator())
    GeneratorRegistry.register(GroqTextGenerator())
    GeneratorRegistry.register(GeminiTextGenerator())

    # Future Scope Multimodal Modules
    GeneratorRegistry.register(CausalVAEImageGenerator())
    GeneratorRegistry.register(CausalVideoDiffusionGenerator())
