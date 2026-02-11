from typing import Optional, Sequence

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_pca_scatter(
    pca_df: pd.DataFrame,
    cluster_col: str = "Cluster",
    title: str = "PCA Projection",
    save_path: Optional[str] = None,
) -> None:
    """
    Generic 2D PCA scatterplot coloured by cluster labels.
    Expects columns ['PC1', 'PC2', cluster_col] in pca_df.
    """
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=pca_df,
        x="PC1",
        y="PC2",
        hue=cluster_col,
        palette="Set2",
        alpha=0.8,
    )
    plt.title(title)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_centroid_heatmap(
    centroids: pd.DataFrame,
    markers: Optional[Sequence[str]] = None,
    title: str = "Cluster Centroids (Key Markers)",
    save_path: Optional[str] = None,
) -> None:
    """
    Heatmap of cluster centroids for a subset of clinically important markers.
    """
    if markers is not None:
        available = [m for m in markers if m in centroids.columns]
        centroids = centroids[available]

    plt.figure(figsize=(8, 4))
    sns.heatmap(centroids, cmap="coolwarm", center=0, annot=True, fmt=".2f")
    plt.title(title)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_before_after_histogram(
    before: "pd.Series",
    after: "pd.Series",
    feature_name: str = "Feature",
    title: str = "Before vs After Transformation",
    save_path: Optional[str] = None,
) -> None:
    """
    Side-by-side histograms comparing raw vs transformed distribution of one feature.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(before.dropna(), bins=30, color="gray", alpha=0.7, edgecolor="white")
    axes[0].set_title(f"{feature_name} (Before)")
    axes[0].set_xlabel("Value")
    axes[0].set_ylabel("Count")
    axes[1].hist(after.dropna(), bins=30, color="#2ecc71", alpha=0.7, edgecolor="white")
    axes[1].set_title(f"{feature_name} (After)")
    axes[1].set_xlabel("Value")
    axes[1].set_ylabel("Count")
    plt.suptitle(title)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_icu_rate(
    df: pd.DataFrame,
    cluster_col: str,
    icu_col: str,
    title: str = "ICU Admission Rate by Cluster",
    save_path: Optional[str] = None,
) -> None:
    """
    Bar chart of ICU admission rate per cluster.
    """
    if icu_col not in df.columns:
        raise KeyError(f"ICU column '{icu_col}' not found in dataframe.")

    icu_rate = df.groupby(cluster_col)[icu_col].mean() * 100

    plt.figure(figsize=(6, 4))
    sns.barplot(x=icu_rate.index.astype(str), y=icu_rate.values, color="#e67e22")
    plt.title(title)
    plt.xlabel("Cluster")
    plt.ylabel("ICU Admission Rate (%)")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    plt.show()

