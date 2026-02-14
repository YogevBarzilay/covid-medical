"""
Model Evaluation Module for Phenotype Validation

This module provides the `PhenotypeValidator` class for validating
clustered phenotypes using supervised learning and feature importance analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


class PhenotypeValidator:
    """
    Validates clustered phenotypes using supervised classification.
    
    This class trains a Random Forest classifier to predict phenotype labels
    from clinical features, providing accuracy metrics and feature importance
    analysis.
    """
    
    def __init__(self, df):
        """
        Initialize the validator with a dataframe.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataset containing features and phenotype labels.
        """
        self.df = df.copy()
        self.model = None
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def train_classifier(self, target_col='Phenotype'):
        """
        Train a Random Forest classifier to predict phenotypes.
        
        Preprocessing:
        - Drops non-numeric columns (like IDs), the target column, and 'Cluster' column
          (to prevent data leakage, since Phenotype is derived from Cluster)
        - Handles NaNs by filling with 0
        
        Model:
        - RandomForestClassifier with 100 estimators
        
        Train/Test Split:
        - 80% train, 20% test
        
        Parameters
        ----------
        target_col : str, default='Phenotype'
            Name of the target column containing phenotype labels.
            
        Returns
        -------
        accuracy : float
            Accuracy score on the test set.
        report : str
            Classification report (text format).
        """
        # Prepare features (X) and target (y)
        if target_col not in self.df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataframe.")
        
        y = self.df[target_col]
        
        # Drop target column and 'Cluster' column to prevent data leakage
        # (Phenotype is derived from Cluster, so including Cluster would be cheating)
        X = self.df.drop(columns=[target_col, 'Cluster'], errors='ignore')
        
        # Keep only numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        X = X[numeric_cols]
        
        # Handle NaNs: fill with 0
        X = X.fillna(0)
        
        # Train/test split (80/20)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Store feature names AFTER split to ensure exact match with model
        # (X_train.columns should match the order of feature_importances_)
        self.feature_names = self.X_train.columns.tolist()
        
        # Initialize and train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_pred = self.model.predict(self.X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred)
        
        return accuracy, report
    
    def plot_feature_importance(self, top_n=10):
        """
        Create a horizontal bar plot of top N feature importances.
        
        Parameters
        ----------
        top_n : int, default=10
            Number of top features to display.
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            The figure object containing the plot.
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_classifier() first.")
        
        if self.feature_names is None:
            raise ValueError("Feature names not found. Call train_classifier() first.")
        
        # Extract feature importances
        importances = self.model.feature_importances_
        
        # Safety check: ensure feature_names and importances have matching lengths
        if len(self.feature_names) != len(importances):
            raise ValueError(
                f"Mismatch between feature names ({len(self.feature_names)}) "
                f"and importances ({len(importances)}). "
                "This should not happen if train_classifier() was called correctly."
            )
        
        # Create DataFrame for easier plotting
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False).head(top_n)
        
        # Create horizontal bar plot
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=importance_df,
            y='feature',
            x='importance',
            ax=ax,
            palette='viridis'
        )
        ax.set_xlabel('Feature Importance')
        ax.set_ylabel('Feature')
        ax.set_title(f'Top {top_n} Feature Importances')
        plt.tight_layout()
        
        return fig
    
    def check_viral_coinfection(self, viral_cols):
        """
        Calculate percentage of positive viral cases within each phenotype.
        
        Parameters
        ----------
        viral_cols : list of str
            List of column names containing viral test results.
            Positive cases are assumed to be value=1 or string='detected'.
            
        Returns
        -------
        summary_df : pd.DataFrame
            DataFrame with columns: Phenotype, Virus, Percentage_Positive
        """
        if 'Phenotype' not in self.df.columns:
            raise ValueError("'Phenotype' column not found. Ensure phenotypes are mapped.")
        
        results = []
        
        for virus_col in viral_cols:
            if virus_col not in self.df.columns:
                continue
            
            # Group by phenotype
            for phenotype in self.df['Phenotype'].unique():
                mask = self.df['Phenotype'] == phenotype
                subset = self.df.loc[mask, virus_col]
                
                # Count positive cases (1 or 'detected')
                if subset.dtype == 'object':
                    # String column: check for 'detected' or similar
                    positive = subset.str.contains('detected|positive|yes', case=False, na=False).sum()
                else:
                    # Numeric column: check for 1
                    positive = (subset == 1).sum()
                
                total = len(subset.dropna())
                pct = (positive / total * 100) if total > 0 else 0.0
                
                results.append({
                    'Phenotype': phenotype,
                    'Virus': virus_col,
                    'Percentage_Positive': pct,
                    'Count_Positive': positive,
                    'Total': total
                })
        
        summary_df = pd.DataFrame(results)
        return summary_df
