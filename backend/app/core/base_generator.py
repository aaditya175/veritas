"""
Veritas Core Architecture: Base Generator Interfaces
Defines abstract interfaces for multimodal generative models (Tabular, Text, Image, Video).
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
import pandas as pd


class Modality(str, Enum):
    TABULAR = "tabular"
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class BaseGenerator(ABC):
    """Abstract base class for all generative model plugins in Veritas."""
    name: str = "base"
    display_name: str = "Base Generator"
    modality: Modality = Modality.TABULAR
    description: str = ""
    is_available: bool = True
    supports_counterfactual: bool = False
    is_future_scope: bool = False

    @abstractmethod
    def fit(self, data: Any, **kwargs) -> Any:
        """Fit the generative model on input training data."""
        pass

    @abstractmethod
    def sample(self, n: int, **kwargs) -> Any:
        """Generate n synthetic samples."""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Return generator metadata for API reflection and UI discovery."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "modality": self.modality.value,
            "description": self.description,
            "is_available": self.is_available,
            "supports_counterfactual": self.supports_counterfactual,
            "is_future_scope": self.is_future_scope
        }


class BaseTabularGenerator(BaseGenerator):
    """Abstract interface for all Tabular / CSV generators."""
    modality: Modality = Modality.TABULAR

    @abstractmethod
    def fit(self, df: pd.DataFrame, causal_graph: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Fit on pandas DataFrame and optional user-reviewed causal DAG."""
        pass

    @abstractmethod
    def sample(self, n: int, **kwargs) -> pd.DataFrame:
        """Generate n synthetic rows as a pandas DataFrame."""
        pass

    def intervene(self, row: Dict[str, Any], target_col: str, new_value: Any) -> Dict[str, Any]:
        """
        Counterfactual intervention: Pearl-style abduction -> action -> prediction.
        Overridden by causal generators; baseline generators report fallback or unsupported.
        """
        raise NotImplementedError(f"Generator {self.name} does not support structural counterfactuals.")


class BaseTextGenerator(BaseGenerator):
    """Abstract interface for all Text corpus generators."""
    modality: Modality = Modality.TEXT

    @abstractmethod
    def generate(
        self,
        corpus_texts: List[str],
        sample_count: int = 5,
        bias_category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate synthetic text items following style, length, and label distributions."""
        pass


class BaseImageGenerator(BaseGenerator):
    """
    Multimodal Future Scope: Image Generator interface.
    Architected for future CausalLatentGenerator / CausalVAE modules without refactoring.
    """
    modality: Modality = Modality.IMAGE
    is_future_scope: bool = True

    @abstractmethod
    def fit(self, data: Any, **kwargs) -> Any:
        pass

    @abstractmethod
    def sample(self, n: int, **kwargs) -> Any:
        pass

    def intervene_latent(self, image_id: str, latent_factor: str, target_val: float) -> Any:
        """Future hook: intervene on interpretable causal factors (e.g., lighting, rotation, pose)."""
        raise NotImplementedError("Image generation is scheduled for Phase 4 Multimodal release.")


class BaseVideoGenerator(BaseGenerator):
    """
    Multimodal Future Scope: Video Generator interface.
    Architected for temporal causal structural diffusion modules.
    """
    modality: Modality = Modality.VIDEO
    is_future_scope: bool = True

    @abstractmethod
    def fit(self, data: Any, **kwargs) -> Any:
        pass

    @abstractmethod
    def sample(self, n: int, **kwargs) -> Any:
        pass
