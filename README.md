## covid-medical

### Clinical ERD & Data Pipeline

```mermaid
flowchart LR
    %% Entities
    RAW[\"Raw Data\\n(Einstein Data4u CSV)\"]:::raw

    subgraph Logical Entities
        P[\"Patient\\n- Patient ID\\n- Age quantile\\n- Unit (ICU / Ward)\"]:::entity
        B[\"Biomarkers\\n- Blood test panel\\n- Lab features\"]:::entity
        PH[\"Phenotype\\n- Cluster label\\n- Clinical profile\"]:::entity
    end

    %% Pipeline stages
    RAW --> DL[\"Load & Basic Cleaning\"]
    DL --> IMP[\"KNN Imputation\\nKNNImputer(n_neighbors=5)\"]:::stage
    IMP --> TR[\"Distribution Handling\\nPower / Quantile Transform\"]:::stage
    TR --> DR[\"Dimensionality Reduction\\nPCA (95% variance)\"]:::stage
    DR --> CL[\"Clustering\\nK-Means (k=3)\"]:::stage
    CL --> VAL[\"Statistical Validation\\nANOVA / Chi-square\"]:::stage

    %% Links to entities
    DL --> P
    DL --> B
    CL --> PH
    VAL --> PH

    classDef raw fill:#f5f5f5,stroke:#666,stroke-width:1px;
    classDef entity fill:#e8f4ff,stroke:#2b6cb0,stroke-width:1px;
    classDef stage fill:#e6fffa,stroke:#2c7a7b,stroke-width:1px;
```

This ERD and flow describe how the flat hospital CSV is mapped into logical entities (`Patient`, `Biomarkers`, `Phenotype`) and processed through the clinical ML pipeline (imputation → transformation → PCA → clustering → validation).