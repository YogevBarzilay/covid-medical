from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, GaussianMixture

from .visualization import plot_pca_scatter


@dataclass
class ClinicalClustering:
    """
    Wrapper around unsupervised clustering algorithms for clinical phenotyping.

    Supports:
    - K-Means (default, k=3)
    - Gaussian Mixture Models (GMM)

    This class is intentionally lightweight: it expects preprocessed features
    (e.g. output of ClinicalPreprocessor).
    """

    n_clusters: int = 3
    method: str = "kmeans"  # "kmeans" or "gmm"
    random_state: int = 42

    def __post_init__(self):
        method = self.method.lower()
        if method == "kmeans":
            self._model = KMeans(
                n_clusters=self.n_clusters,
                random_state=self.random_state,
                n_init=10,
            )
        elif method == "gmm":
            self._model = GaussianMixture(
                n_components=self.n_clusters,
                random_state=self.random_state,
            )
        else:
            raise ValueError(f"Unsupported method='{self.method}'. Use 'kmeans' or 'gmm'.")

    def fit_predict(self, X: pd.DataFrame) -> np.ndarray:
        if isinstance(self._model, KMeans):
            return self._model.fit_predict(X)
        else:
            self._model.fit(X)
            return self._model.predict(X)

    @property
    def model(self):
        return self._model

    def plot_pca(
        self,
        X_pca: pd.DataFrame,
        labels: np.ndarray,
        title: str = "PCA Projection: Clinical Clusters",
        save_path: Optional[str] = None,
    ) -> None:
        """
        Convenience wrapper to plot a 2D PCA scatter coloured by cluster labels.
        Expects X_pca with columns ['PC1', 'PC2'].
        """
        df = X_pca.copy()
        df["Cluster"] = labels.astype(str)
        plot_pca_scatter(df, cluster_col="Cluster", title=title, save_path=save_path)

