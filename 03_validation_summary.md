### `03_validation.ipynb` – Technical Summary

---

## 1. Data loading and setup

- **Input file**: `../data/processed/02_clustered_data.csv`
- **Libraries**:
  - `pandas`, `numpy`, `seaborn`, `matplotlib.pyplot`
  - `scipy.stats.chi2_contingency`, `scipy.stats.kruskal`
- **Style**: `seaborn.set_style("whitegrid")` for publication-quality plots.

---

## 2. Clinical Outcome: ICU Admission (Gold Standard)

- **Target variable**: `Patient addmited to intensive care unit (1=yes, 0=no)` (binary).
- **Test**: Chi-Square (`chi2_contingency`) on the crosstab of ICU admission vs Cluster.
- **Visualization**: Stacked Bar Chart (normalized to 100%) – proportion of ICU vs Not ICU per cluster.
- **Annotation**: ICU admission rates printed per cluster (e.g., Cluster 0: 2.5%, Cluster 1: 5.8%, Cluster 2: 10%).

**Interpretation**:
- Significant association (p ≈ 0.002): clusters differ in ICU risk.
- Cluster 2 has the highest ICU rate (≈10%), supporting the "Severe/Critical" label.

---

## 3. Biomarker Analysis (Biological Profile)

### 3.1 Selected features (from screening)

- `selected_features = ['Rods #', 'Hemoglobin', 'Hematocrit', 'Basophils', 'Urea', 'Creatinine']`
- If any are missing, `Lactic Dehydrogenase` is used as fallback.

### 3.2 Statistical tests

- **Kruskal-Wallis** for each feature (non-parametric, compares distributions across 3 clusters).
- p-values printed per feature (e.g., Rods #: 4.92e-45, Hemoglobin: 6.46e-21).

### 3.3 Visualization

- **Grid of boxplots** (2 rows × 3 columns) – each subplot shows the distribution of one biomarker by Cluster.
- Colors: Cluster 0 (green), Cluster 1 (orange), Cluster 2 (red).
- Figure saved: `figures/biomarker_boxplots_by_cluster.png`.

---

## 4. Clinical Interpretation (The Story)

| Cluster | Phenotype        | Summary                                                                 |
|---------|------------------|-------------------------------------------------------------------------|
| **0**   | Mild             | Low ICU rate, normal blood counts.                                     |
| **1**   | Moderate         | Intermediate ICU risk, mixed biomarker profile.                        |
| **2**   | Severe/Critical  | Highest ICU risk, elevated Rods # (Left Shift immune response), low Hemoglobin. |

---

## 5. Outputs

- **Data**: `data/processed/cluster_descriptions.csv` – mapping of Cluster → Phenotype → Description.
- **Figures**:
  - `figures/icu_admission_by_cluster.png` – stacked bar of ICU admission by cluster.
  - `figures/biomarker_boxplots_by_cluster.png` – biomarker boxplots by cluster.

These outputs provide a clear validation story: the clusters differ in both outcome (ICU) and biology (blood markers), supporting the Mild / Moderate / Severe interpretation used in `04_supervised_validation.ipynb`.
