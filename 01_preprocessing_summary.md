## 01 – Clinical Data Preprocessing (Summary)

This document summarizes the logic, steps, and outputs of the `01_preprocessing.ipynb` notebook.  
It explains how we go from a raw Excel cohort to a clean, analysis‑ready dataset used later for PCA, clustering, and validation.

---

## 1. Data Loading and Structure

- **Raw source**: `../data/raw/dataset.xlsx` (loaded via `ClinicalDataLoader`).
- **Output file**: `../data/processed/01_cleaned_advanced.csv`.
- **Figures directory**: `../figures/`.
- **Loader**:
  - Uses `ClinicalDataLoader(DATA_PATH)` to read the Excel file.
  - Applies cohort‑level filters:
    - `min_labs=10`: keep patients with at least 10 lab measurements.
    - `max_missing=0.9`: drop features that are almost entirely missing (more than 90% missing).
  - Returns:
    - `features`: numeric lab variables.
    - `meta`: patient‑level metadata (IDs, demographics, possibly admission info).
  - A combined `df = [meta | features]` is created.

**Key numbers printed:**
- `Loaded: N rows, M columns` – after the basic cohort filtering (patients + features).

This defines the **working cohort** and feature set that all later notebooks (PCA, clustering, validation) build upon.

---

## 2. Preprocessing Pipeline (KNN + QuantileTransformer)

The core preprocessing is handled by `ClinicalPreprocessor` from `src.features`:

- **Configuration**:
  - `n_neighbors=5` – KNN imputer uses the 5 most similar patients to impute missing values.
  - `output_distribution="normal"` – `QuantileTransformer` maps each variable to an approximately Gaussian distribution.

- **Steps inside `fit_transform(features)`**:
  1. **KNN Imputation**  
     - For each lab variable, missing values are filled based on similar patients in the multivariate space.
     - This preserves realistic combinations of lab values and avoids simple mean/median imputation.
  2. **Distributional Transformation (`QuantileTransformer`)**  
     - Each lab is transformed to a smoother, more Gaussian‑like distribution.
     - Reduces skewness, heavy tails, and extreme outliers.
     - Makes the data better suited for:
       - PCA (which assumes variance structure in roughly symmetric variables).
       - Distance‑based clustering (K‑Means, GMM).

- **Outputs**:
  - `X_clean`: fully imputed + transformed features in the original feature space.
  - `X_pca`: PCA‑space representation (not saved here, but used downstream in `02_pca_clustering.ipynb`).

The notebook then reconstructs a dataframe:

- `output = meta.copy()`
- For each column in `X_clean`, add it into `output`.
- Save to CSV: `01_cleaned_advanced.csv` (this is the **main input** to the PCA/clustering notebook).

---

## 3. Data Quality & Transformation Audit

To justify preprocessing choices and provide transparency, the notebook includes several visual “audit” plots.

### 3.1 Missing Values Map

- **Figure**: `missing_values_map.png`
- **Computation**:
  - `missing_pct = features.isna().mean() * 100`
  - Horizontal bar plot of `% Missing` per feature.
- **Interpretation**:
  - Shows which lab tests are well measured (low missingness) vs. rarely measured.
  - Justifies dropping features with extremely high missingness and motivates the use of imputation.

**Clinical/statistical message**:  
We want to avoid basing analyses on lab tests that are measured in only a tiny fraction of patients and to be transparent about the amount of missingness we need to handle.

### 3.2 Before vs. After Distribution Grid

- **Figure**: `before_after_distribution_grid.png` (grid created via `plot_before_after_histogram`).
- **Content**:
  - For selected key markers (e.g. Leukocytes, Creatinine, Platelets), the grid compares:
    - **Left column**: raw distributions (skewed, long‑tailed, with outliers).
    - **Right column**: post‑preprocessing distributions (after KNN imputation + QuantileTransformer).

**Interpretation**:
- The right‑hand histograms are more symmetric and closer to Gaussian.
- Extreme outliers are dampened, and the bulk of the cohort is more “balanced”.
- This transformation makes the dataset more appropriate for:
  - Linear projections (PCA).
  - Distance‑based clustering, which is sensitive to scale and extreme values.

### 3.3 Correlation / Structure Preservation (if present)

If additional plots are present (e.g., correlation matrices before/after), they are meant to show that:
- Key correlation patterns between lab markers are **largely preserved** despite transformation.
- The goal is not to distort clinical relationships, but to regularize scale and distribution so that multivariate structure is easier to capture.

---

## 4. Cohort Selection: Data Retention

- **Figure**: `cohort_selection_funnel.png`
- **Computation**:
  - `raw_df = pd.read_excel(DATA_PATH)` → `n_raw` (total patients in the original file).
  - `n_final = len(df)` → patients retained after:
    - Minimum number of lab tests (≥10).
    - Feature and missingness filters.
  - Bar plot with:
    - `Total Patients`.
    - `Final Cohort (>10 exams)`.
  - Annotates each bar with:
    - Absolute count.
    - Percentage of original sample retained.

**Interpretation**:
- Quantifies how much of the original cohort is excluded due to data quality constraints.
- Ensures transparency: we can report to clinicians how many patients were dropped and why.
- The retained cohort represents patients with **sufficient longitudinal lab information** for robust phenotype discovery.

---

## 5. Outputs for Downstream Notebooks

The key artifacts produced by `01_preprocessing.ipynb` and used later are:

- **Processed dataset**:
  - `01_cleaned_advanced.csv`
  - Contains:
    - Patient metadata (IDs, demographics).
    - Fully imputed, transformed lab features (one row per patient).
  - This file is the **starting point** for:
    - `02_pca_clustering.ipynb` (PCA + K‑Means phenotyping).
    - `03_validation.ipynb` (validation and clinical outcome analyses).

- **Figures for the report**:
  - `missing_values_map.png` – missingness profile.
  - `before_after_distribution_grid.png` – effect of the preprocessing pipeline on distributions.
  - `cohort_selection_funnel.png` – patient retention funnel.

These outputs together provide a **transparent and clinically interpretable preprocessing story**:
- Which patients and lab tests are included.
- How missing data and skewed distributions are handled.
- Why the resulting dataset is appropriate for advanced statistical modeling and machine learning in subsequent notebooks.

