### `02_pca_clustering.ipynb` – Technical Summary

---

## 1. Data loading and setup

- **Input file**: `../data/processed/01_cleaned_advanced.csv`
- **Libraries**:
  - `pandas`, `matplotlib.pyplot`
  - `sklearn.decomposition.PCA`
  - `sklearn.cluster.KMeans`
  - `src.models.ClinicalClustering`
  - `src.visualization.plot_pca_scatter`, `plot_centroid_heatmap`
- **Paths**:
  - Output clustered data: `../data/processed/02_clustered_data.csv`
  - Figures directory: `../figures/`

---

## 2. Feature selection and PCA

- From the full dataframe `df`, the notebook:
  - **Excludes**: `Patient ID`, `SARS-Cov-2 exam result`, `Patient age quantile`, and hospitalization flags (regular ward, semi-intensive, ICU).
  - Keeps only **numeric** columns among the remaining → `feature_cols`.
  - Creates feature matrix `X = df[feature_cols]`.
  - Data from `01_cleaned_advanced.csv` is already preprocessed (KNN imputation + QuantileTransformer), so no additional scaling is applied before PCA.

- **PCA**:
  - PCA fit on `X` with `PCA(n_components=0.95, random_state=42)`.
  - Retains components for **95% of variance**.
  - Output: `X_pca` (DataFrame with columns `PC1`, `PC2`, ..., `PCn`).

---

## 3. Clustering: K-Means (k=3)

### 3.1 Primary clustering choice

- **K-Means (k=3)** was selected as the production clustering model.
- Model selection experiments (K-Means vs GMM vs Hierarchical) were performed in `experiments/02_clustering_model_sweep.ipynb`, where we evaluate Silhouette scores, GMM BIC, and dendrograms across k=2..8.
- Based on that sweep, K-Means was chosen for interpretability and suitability to hard cluster assignments.
- k=3 provides **clinically interpretable subgroups** (e.g., Mild / Moderate / Severe phenotypes) suitable for downstream validation.

### 3.2 Core K-Means model

- Uses `ClinicalClustering(n_clusters=3, method="kmeans")` (wrapper around `KMeans`).
- Fit and predict on `X_pca`.
- Output: cluster labels 0, 1, 2 for each patient.
- `df_out` = copy of `df` with added column `Cluster`.
- Saved to `02_clustered_data.csv`.

---

## 4. Visualizations

- **Elbow method** (`figures/elbow_kmeans_pca.png`):
  - Inertia vs k (1..10) to justify k=3.
  - Vertical line at k=3 ("Clinical Granularity").

- **PCA scatter** (`figures/pca_kmeans_k3.png`):
  - PC1 vs PC2 colored by cluster.
  - Title: "PCA Projection: K-Means k=3".

- **Centroid heatmap** (`figures/centroid_heatmap_k3.png`):
  - Mean of original features per cluster for key markers: Leukocytes, Hemoglobin, Platelets, Lymphocytes, Neutrophils, Urea, Creatinine.
  - Title: "Cluster Centroids (Key Markers): Clinical Story".

---

## 5. Outputs

- **Data**: `data/processed/02_clustered_data.csv` – full patient data with `Cluster` column (values 0, 1, 2).
- **Figures**:
  - `figures/elbow_kmeans_pca.png` – Elbow method.
  - `figures/pca_kmeans_k3.png` – PCA scatter by cluster.
  - `figures/centroid_heatmap_k3.png` – Centroid heatmap of key markers.

These outputs feed into `03_validation.ipynb` for statistical testing (e.g., cluster–outcome associations, ICU rates by phenotype).
