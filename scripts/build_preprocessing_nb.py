import json

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Clinical Data Preprocessing\n",
                "\n",
                "Load → Split → Impute/Scale (KNN + QuantileTransformer) → Save",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "\n",
                "ROOT = Path.cwd().parent\n",
                "if str(ROOT) not in sys.path:\n",
                "    sys.path.insert(0, str(ROOT))\n",
                "\n",
                "from src.data_loader import ClinicalDataLoader\n",
                "from src.features import ClinicalPreprocessor\n",
                "\n",
                "RAW_PATH = Path(\"../data/raw/dataset.xlsx\")\n",
                "OUT_PATH = Path(\"../data/processed/01_cleaned_advanced.csv\")\n",
                "FIG_DIR = Path(\"../figures\")\n",
                "OUT_PATH.parent.mkdir(parents=True, exist_ok=True)\n",
                "FIG_DIR.mkdir(parents=True, exist_ok=True)\n",
                "\n",
                "# Pipeline: Load -> Split -> Impute/Scale\n",
                "loader = ClinicalDataLoader(RAW_PATH)\n",
                "features, meta = loader.load_cohort(min_labs=10, max_missing=0.9)\n",
                "\n",
                "preprocessor = ClinicalPreprocessor(n_neighbors=5, output_distribution=\"normal\")\n",
                "X_transformed, _ = preprocessor.fit_transform(features)\n",
                "\n",
                "# Combine with metadata for downstream use\n",
                "output = meta.copy()\n",
                "for c in X_transformed.columns:\n",
                "    output[c] = X_transformed[c].values\n",
                "\n",
                "output.to_csv(OUT_PATH, index=False)\n",
                "print(f\"Saved: {OUT_PATH} | Shape: {output.shape}\")",
            ],
            "outputs": [],
            "execution_count": None,
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Before vs After: Leukocytes\n",
                "\n",
                "The histogram proves that the QuantileTransformer normalizes the distribution.",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": [
                "from src.visualization import plot_before_after_histogram\n",
                "\n",
                "feat_name = \"Leukocytes\"\n",
                "if feat_name in features.columns and feat_name in X_transformed.columns:\n",
                "    plot_before_after_histogram(\n",
                "        features[feat_name],\n",
                "        X_transformed[feat_name],\n",
                "        feature_name=feat_name,\n",
                "        title=\"Leukocytes: Before vs After KNN Imputation + QuantileTransformer\",\n",
                "        save_path=str(FIG_DIR / \"leukocytes_before_after.png\"),\n",
                "    )\n",
                "else:\n",
                "    print(f\"'{feat_name}' not found. Available: {list(features.columns[:5])}...\")",
            ],
            "outputs": [],
            "execution_count": None,
        },
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

p = Path(__file__).resolve().parent.parent / "notebooks" / "01_preprocessing.ipynb"
with open(p, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Created:", p)
