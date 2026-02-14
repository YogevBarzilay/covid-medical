import pandas as pd
from pathlib import Path
from typing import Tuple


class ClinicalDataLoader:
    """
    Load raw Einstein Data4u exports and apply light, schema-level cleaning.

    Responsibilities:
    - Read Excel/CSV from data/raw
    - Normalise column names
    - Ensure key columns (Patient ID, age, targets) exist
    - Split into features/metadata for downstream processing
    """

    def __init__(self, raw_path: Path):
        self.raw_path = Path(raw_path)

    def load(self) -> pd.DataFrame:
        if self.raw_path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(self.raw_path)
        else:
            df = pd.read_csv(self.raw_path)

        # Normalise column names (spaces, non-breaking spaces, etc.)
        df.columns = (
            df.columns.astype(str)
            .str.replace("\xa0", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        return df

    def load_and_split(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns:
            features: numeric lab features only (no IDs / targets / age)
            meta: patient-level metadata and targets
        """
        df = self.load()

        id_cols = ["Patient ID"]
        target_cols = [
            "SARS-Cov-2 exam result",
            "Patient addmited to regular ward (1=yes, 0=no)",
            "Patient addmited to semi-intensive unit (1=yes, 0=no)",
            "Patient addmited to intensive care unit (1=yes, 0=no)",
        ]
        age_cols = ["Patient age quantile"]

        protected = {c for c in id_cols + target_cols + age_cols if c in df.columns}
        numeric_cols = [
            c for c in df.columns if c not in protected and pd.api.types.is_numeric_dtype(df[c])
        ]

        features = df[numeric_cols].copy()
        meta = df[list(protected)].copy()
        return features, meta

    def load_cohort(
        self,
        min_labs: int = 10,
        max_missing: float = 0.9,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load, apply cohort selection (>= min_labs per patient), drop features
        with > max_missing fraction, and return (features, meta).
        """
        df = self.load()
        protected = {"Patient ID", "SARS-Cov-2 exam result", "Patient age quantile"}
        protected |= {
            "Patient addmited to regular ward (1=yes, 0=no)",
            "Patient addmited to semi-intensive unit (1=yes, 0=no)",
            "Patient addmited to intensive care unit (1=yes, 0=no)",
        }
        numeric_cols = [
            c
            for c in df.columns
            if c not in protected and pd.api.types.is_numeric_dtype(df[c])
        ]
        patient_counts = df[numeric_cols].notna().sum(axis=1)
        df = df.loc[patient_counts >= min_labs].copy()
        missing_frac = df[numeric_cols].isna().mean()
        kept = missing_frac[missing_frac < max_missing].index.tolist()
        features = df[kept].copy()
        meta = df[[c for c in protected if c in df.columns]].copy()
        return features, meta

