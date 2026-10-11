"""
Veritas Statistical Baseline: Gaussian Copula Synthesizer
Uses SDV's GaussianCopulaSynthesizer to model multivariate dependencies via joint copula distributions.
"""
import pandas as pd
from typing import Dict, Any, Optional
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer
from app.core.base_generator import BaseTabularGenerator, Modality


class GaussianCopulaGenerator(BaseTabularGenerator):
    name = "gaussian_copula"
    display_name = "Gaussian Copula (Statistical)"
    modality = Modality.TABULAR
    description = "Statistical baseline fitting marginal distributions per column and a multivariate Gaussian copula for cross-feature dependencies."
    supports_counterfactual = False

    def __init__(self):
        self.synthesizer: Optional[GaussianCopulaSynthesizer] = None
        self.metadata: Optional[SingleTableMetadata] = None
        self.fitted = False

    def fit(self, df: pd.DataFrame, causal_graph: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(df)

        self.synthesizer = GaussianCopulaSynthesizer(self.metadata)
        self.synthesizer.fit(df)
        self.fitted = True
        return self

    def sample(self, n: int, **kwargs) -> pd.DataFrame:
        if not self.fitted or self.synthesizer is None:
            raise RuntimeError("GaussianCopulaGenerator must be fitted before sampling.")
        synthetic_df = self.synthesizer.sample(num_rows=n)
        return synthetic_df
