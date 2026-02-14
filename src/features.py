from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import QuantileTransformer
from sklearn.decomposition import PCA


@dataclass
class ClinicalPreprocessor:
    """
    End-to-end preprocessing for clinical lab panels:
    - KNN imputation to preserve biomarker relationships
    - Skew handling via QuantileTransformer (Yeo-Johnson / normal output)
    - Optional dimensionality reduction via PCA

    This class is deliberately model-agnostic: it prepares X for clustering
    or downstream supervised models.
    """

    n_neighbors: int = 5
    output_distribution: str = "normal"  # passed to QuantileTransformer
    pca_variance: Optional[float] = None  # e.g. 0.95 for 95% variance

    def __post_init__(self):
        self._imputer: Optional[KNNImputer] = None
        self._transformer: Optional[QuantileTransformer] = None
        self._pca: Optional[PCA] = None

    @property
    def pca_model(self) -> Optional[PCA]:
        return self._pca

    def fit_transform(self, X: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
        """
        Fit all preprocessing steps and return:
            X_transformed: fully imputed + transformed features (same dimension as X)
            X_pca: optional PCA projection (if pca_variance is set), else None
        """
        # KNN imputation
        self._imputer = KNNImputer(n_neighbors=self.n_neighbors)
        imputed = self._imputer.fit_transform(X)

        # Distribution handling (Yeo-Johnson via QuantileTransformer with normal output)
        self._transformer = QuantileTransformer(
            output_distribution=self.output_distribution,
            random_state=42,
        )
        transformed = self._transformer.fit_transform(imputed)
        X_transformed = pd.DataFrame(transformed, columns=X.columns, index=X.index)

        X_pca = None
        if self.pca_variance is not None:
            self._pca = PCA(n_components=self.pca_variance, random_state=42)
            comps = self._pca.fit_transform(X_transformed)
            X_pca = pd.DataFrame(
                comps,
                index=X.index,
                columns=[f"PC{i+1}" for i in range(comps.shape[1])],
            )

        return X_transformed, X_pca

    def transform(self, X: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
        """
        Apply a previously fitted pipeline to new data.
        """
        if self._imputer is None or self._transformer is None:
            raise RuntimeError("ClinicalPreprocessor must be fit before calling transform().")

        imputed = self._imputer.transform(X)
        transformed = self._transformer.transform(imputed)
        X_transformed = pd.DataFrame(transformed, columns=X.columns, index=X.index)

        X_pca = None
        if self._pca is not None:
            comps = self._pca.transform(X_transformed)
            X_pca = pd.DataFrame(
                comps,
                index=X.index,
                columns=[f"PC{i+1}" for i in range(comps.shape[1])],
            )

        return X_transformed, X_pca

