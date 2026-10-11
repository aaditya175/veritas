"""
Veritas VAE Baseline: TVAE (Tabular Variational Autoencoder)
Uses SDV's TVAESynthesizer with variational latent bottleneck and evidence lower bound optimization.
"""
import pandas as pd
from typing import Dict, Any, Optional
from sdv.metadata import SingleTableMetadata
from sdv.single_table import TVAESynthesizer
from app.core.base_generator import BaseTabularGenerator, Modality


class TVAEGenerator(BaseTabularGenerator):
    name = "tvae"
    display_name = "TVAE (Variational Autoencoder)"
    modality = Modality.TABULAR
    description = "Likelihood-based deep autoencoding baseline optimizing ELBO over continuous and categorical embeddings."
    supports_counterfactual = False

    def __init__(self, epochs: int = 50):
        self.epochs = epochs
        self.synthesizer: Optional[TVAESynthesizer] = None
        self.metadata: Optional[SingleTableMetadata] = None
        self.fitted = False

    def fit(self, df: pd.DataFrame, causal_graph: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(df)

        epochs = kwargs.get("epochs", self.epochs)
        self.synthesizer = TVAESynthesizer(self.metadata, epochs=epochs)
        self.synthesizer.fit(df)
        self.fitted = True
        return self

    def sample(self, n: int, **kwargs) -> pd.DataFrame:
        if not self.fitted or self.synthesizer is None:
            raise RuntimeError("TVAEGenerator must be fitted before sampling.")
        return self.synthesizer.sample(num_rows=n)
