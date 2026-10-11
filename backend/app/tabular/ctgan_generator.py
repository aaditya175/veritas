"""
Veritas GAN Baseline: CTGAN (Conditional Tabular GAN)
Uses SDV's CTGANSynthesizer with conditional generator and pac-discriminator.
"""
import pandas as pd
from typing import Dict, Any, Optional
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from app.core.base_generator import BaseTabularGenerator, Modality


class CTGANGenerator(BaseTabularGenerator):
    name = "ctgan"
    display_name = "CTGAN (Conditional GAN)"
    modality = Modality.TABULAR
    description = "Dominant deep generative baseline for tabular data using conditional adversarial networks and mode-specific normalization."
    supports_counterfactual = False

    def __init__(self, epochs: int = 50):
        self.epochs = epochs
        self.synthesizer: Optional[CTGANSynthesizer] = None
        self.metadata: Optional[SingleTableMetadata] = None
        self.fitted = False

    def fit(self, df: pd.DataFrame, causal_graph: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(df)

        epochs = kwargs.get("epochs", self.epochs)
        self.synthesizer = CTGANSynthesizer(self.metadata, epochs=epochs, verbose=False)
        self.synthesizer.fit(df)
        self.fitted = True
        return self

    def sample(self, n: int, **kwargs) -> pd.DataFrame:
        if not self.fitted or self.synthesizer is None:
            raise RuntimeError("CTGANGenerator must be fitted before sampling.")
        return self.synthesizer.sample(num_rows=n)
