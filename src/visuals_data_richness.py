from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    data_path = repo_root / "data" / "processed" / "01_cleaned_data.csv"
    figures_dir = repo_root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    # Use the 37 clinical features: the dataset includes 4 outcome columns at the end.
    if df.shape[1] >= 41:
        feature_columns = df.columns[:37]
    else:
        feature_columns = df.columns[:-4]

    completeness = df[feature_columns].notna().mean().mul(100).sort_values()

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 12))
    ax = sns.barplot(
        x=completeness.values,
        y=completeness.index,
        color="#2ecc71",
        edgecolor="none",
    )
    ax.axvline(100, color="black", linestyle="--", linewidth=1)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percent Non-Null")
    ax.set_ylabel("Clinical Feature")
    ax.set_title("Data Quality: Feature Density in Final Cohort")
    plt.tight_layout()
    plt.savefig(figures_dir / "data_quality_feature_density.png", dpi=300)
    plt.close()

    corr = df[feature_columns].corr(method="pearson")

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        xticklabels=False,
        yticklabels=False,
    )
    plt.title("Biological Correlation Heatmap (Final Cohort)")
    plt.tight_layout()
    plt.savefig(figures_dir / "biological_correlation_heatmap.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    main()
