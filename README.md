# COVID‑19 Severity Phenotyping from Routine Blood Tests

## Project Overview

Early triage of COVID‑19 patients remains challenging: clinicians often lack objective tools to predict who will deteriorate and require intensive care. This project provides an objective triage framework using **only routine admission blood tests**-no imaging or clinical scores required. By deriving data-driven severity phenotypes from a high-dimensional panel of laboratory variables, the analysis supports automated decision-making and personalised risk assessment at the bedside.

The work combines unsupervised clustering (PCA + K‑Means), statistical validation against ICU admission, and supervised prediction (Random Forest) to identify and predict three reproducible phenotypes: Mild, Moderate, and Severe. The full analysis pipeline runs in **under 5 minutes** on a standard machine.

---

## Project Structure

| Directory | Contents |
|-----------|----------|
| `data/raw/` | Original Einstein Data4u export (5,644 patients; Excel/CSV; not tracked in Git). |
| `data/processed/` | Preprocessed cohort: `01_cleaned_advanced.csv`, `02_clustered_data.csv`, `cluster_descriptions.csv`. |
| `notebooks/` | Four main notebooks: 01 preprocessing, 02 PCA and clustering, 03 statistical validation, 04 supervised prediction. |
| `experiments/` | Exploratory notebooks for scaling tests, clustering model selection (K‑Means, GMM, Hierarchical), and biomarker screening. |
| `figures/` | Output figures from the pipeline (see Visualizations below). |
| `src/` | Helper modules: `data_loader.py`, `features.py`, `models.py`, `model_evaluation.py`, `evaluation.py`, `visualization.py`, `visuals_data_richness.py`. |
| `docs/` | Final paper: `Machine_Learning_COVID19_Phenotyping.docx` (Abstract, Introduction, Results, Methods, Discussion). |

### Main Notebooks

- **01_preprocessing.ipynb** - Cohort selection (≥10 lab tests per patient), KNN imputation, QuantileTransformer; outputs `01_cleaned_advanced.csv`.
- **02_pca_clustering.ipynb** - PCA (95% variance), K‑Means k=3; outputs `02_clustered_data.csv` and PCA/centroid figures.
- **03_validation.ipynb** - Chi‑Square test for ICU admission, Kruskal-Wallis for biomarkers; produces ICU and biomarker figures.
- **04_supervised_validation.ipynb** - Random Forest classifier (~95% accuracy) and feature importance analysis.

### Experiments

- **01_ab_test_scaling.ipynb** - Alternative preprocessing and scaling strategies.
- **02_clustering_model_selection.ipynb** - Model comparison across K‑Means, GMM, Hierarchical (Silhouette, BIC, dendrograms).
- **03_clinical_screening_dump.ipynb** - Global biomarker screening; outputs `significance_ranking.csv`.

---

## Results Summary

- **Raw cohort:** 5,644 patients (Einstein Data4u).
- **Analysis cohort:** 603 patients (≥10 lab tests per patient, ≤90% missingness per variable).
- **Cluster distribution:** Mild (N=359), Moderate (N=104), Severe (N=140).
- **ICU admission rates:** 2.5%, 5.8%, 10.0% across clusters (Chi‑Square p=0.0018).
- **Supervised model:** Random Forest ~95% accuracy; top predictors include Metamyelocytes, Rods, Basophils (Left Shift).

---

## Visualizations

Primary validation figures:

- **icu_admission_by_cluster.png** - ICU admission rates by phenotype (stacked bar chart).
- **rf_feature_importance.png** - Feature importance from the Random Forest model.

Additional outputs:

- PCA projections (`pca_kmeans_k3.png`), centroid heatmap (`centroid_heatmap_k3.png`), elbow plot (`elbow_kmeans_pca.png`), confusion matrix (`confusion_matrix_rf.png`), biomarker boxplots (`biomarker_boxplots_by_cluster.png`).

---

## Setup and Installation

1. Install Python 3.10+.
2. (Recommended) Create and activate a virtual environment.
3. From the project root:

```bash
pip install -r requirements.txt
```

Main dependencies: `pandas`, `numpy`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `joblib`, `jupyter`, `openpyxl`.

---

## Running the Analysis

1. Launch Jupyter:

```bash
jupyter notebook
```

2. Execute the notebooks in order:

   - `notebooks/01_preprocessing.ipynb`
   - `notebooks/02_pca_clustering.ipynb`
   - `notebooks/03_validation.ipynb`
   - `notebooks/04_supervised_validation.ipynb`

Each notebook writes outputs to `data/processed/` and `figures/`. The full pipeline completes in under 5 minutes on a standard machine.

---

## Reproducing the Paper Results

The quantitative results in `docs/Machine_Learning_COVID19_Phenotyping.docx` are produced by:

- Cohort and missingness plots: `01_preprocessing.ipynb`
- PCA and clustering: `02_pca_clustering.ipynb` and `experiments/02_clustering_model_selection.ipynb`
- ICU and biomarker validation: `03_validation.ipynb`
- Random Forest metrics and feature importance: `04_supervised_validation.ipynb`

Running the four main notebooks and the experiment notebooks regenerates all tables and figures referenced in the paper.

---

## Contributors

**Amit Filler** - Responsible for the end-to-end preprocessing pipeline, statistical and supervised validation (Chi‑Square, Kruskal‑Wallis, Random Forest), and the final research paper.

**Yogev Hadad** - Focused on initial data exploration, clustering model selection (K-Means, GMM, Hierarchical), and high-impact visualizations.