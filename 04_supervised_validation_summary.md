### `04_supervised_validation.ipynb` – Technical Summary

---

## 1. Purpose and setup

- **Goal**: Validate that the phenotypes from clustering are **distinct, predictable clinical entities**, not statistical noise.
- **Input file**: `../data/processed/02_clustered_data.csv`
- **Libraries**:
  - `pandas`, `numpy`, `matplotlib.pyplot`, `seaborn`
  - `src.model_evaluation.PhenotypeValidator`
- **Paths**: Figures saved to `../figures/`

---

## 2. Phenotype mapping

- Based on findings from `03_validation.ipynb`, clusters are mapped to clinical labels:

  | Cluster | Phenotype                          |
  |---------|------------------------------------|
  | 0       | Mild / Resilient                   |
  | 1       | Viral Sepsis (Immune Suppressed)   |
  | 2       | Cytokine Storm (High Risk)         |

- Column `Phenotype` is created from `Cluster` via this mapping.

---

## 3. ML validation (Random Forest)

- **Model**: Random Forest Classifier (`PhenotypeValidator`).
- **Target**: `Phenotype` (3-class).
- **Features**: Numeric clinical/lab columns (excluding IDs, outcomes, etc.).
- **Evaluation**: Accuracy, precision, recall, F1-score per class.

**Typical result**: ~96% accuracy – phenotypes are highly predictable from lab data.

**Interpretation**:
- If accuracy > 90%: phenotypes are distinct and clinically meaningful.
- If accuracy 75–90%: phenotypes are distinguishable but overlap.
- If accuracy < 75%: phenotypes may not be well separated.

---

## 4. Feature importance

- **Method**: Random Forest `feature_importances_`.
- **Visualization**: Bar plot of top N features (e.g., top 15).
- **Figure**: `figures/feature_importance.png`.

**Typical top drivers**: Metamyelocytes, Rods #, Basophils, Myelocytes, Monocytes, Eosinophils, Base excess, Hematocrit, HCO3, Creatinine – consistent with the biomarker story from the screening and validation notebooks.

---

## 5. Viral coinfection analysis (optional)

- **Purpose**: Test whether "Viral Sepsis" phenotype has higher viral coinfection rates.
- **Method**: Search for viral columns (Influenza A/B, Rhinovirus/Enterovirus, etc.) and compute % positive per phenotype.
- **Visualization**: Heatmap of % positive by Virus × Phenotype (`figures/viral_coinfection_heatmap.png`).

**Note**: In the Einstein COVID-19 dataset, viral coinfection columns may be absent; in that case the analysis is skipped.

---

## 6. Outputs

- **Figures**:
  - `figures/feature_importance.png` – top clinical features driving phenotype prediction.
  - `figures/viral_coinfection_heatmap.png` – viral coinfection rates by phenotype (if viral columns exist).

- **Conclusion**: High Random Forest accuracy confirms that the three phenotypes are **distinct, predictable entities** that can be recovered from laboratory markers, supporting the biological validity of the clustering.
