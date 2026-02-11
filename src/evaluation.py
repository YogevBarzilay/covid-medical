from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def anova_by_cluster(
    df: pd.DataFrame,
    cluster_col: str,
    features: List[str],
) -> pd.DataFrame:
    """
    Run one-way ANOVA for each feature across clusters.

    Returns a dataframe with F-statistic and p-value per feature.
    """
    results = []
    for feat in features:
        if feat not in df.columns:
            continue
        groups = [g[feat].dropna().values for _, g in df.groupby(cluster_col)]
        if len(groups) < 2:
            continue
        F, p = stats.f_oneway(*groups)
        results.append({"feature": feat, "F": F, "pvalue": p})

    return pd.DataFrame(results).sort_values("pvalue")


def chi_square_cluster_vs_target(
    df: pd.DataFrame,
    cluster_col: str,
    target_col: str,
) -> Tuple[float, float, int, np.ndarray]:
    """
    Chi-square test of independence between cluster labels and a categorical target.
    Returns the standard scipy.stats.chi2_contingency output.
    """
    contingency = pd.crosstab(df[cluster_col], df[target_col])
    return stats.chi2_contingency(contingency.values)

