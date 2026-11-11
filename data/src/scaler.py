"""
Leakage-Safe Normalization and Scaling Module
Author: Kartikeya Singh (Member 1)
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class LeakageSafeScaler:
    """
    StandardScaler fitted ONLY on baseline/training data splits.
    Ensures zero test-set information leaks into normalization.
    """
    def __init__(self, feature_cols: Optional[List[str]] = None):
        self.feature_cols = feature_cols or [
            "heart_rate_bpm", "spo2_percent", "ambient_temperature_c", "humidity_percent", "aqi"
        ]
        self.means: Dict[str, float] = {}
        self.stds: Dict[str, float] = {}
        self.is_fitted: bool = False

    def fit(self, train_df: pd.DataFrame) -> "LeakageSafeScaler":
        """Compute mean and std on training baseline split only."""
        for col in self.feature_cols:
            if col in train_df.columns:
                valid_data = train_df[col].dropna()
                if len(valid_data) > 0:
                    self.means[col] = float(valid_data.mean())
                    std = float(valid_data.std())
                    self.stds[col] = std if std > 1e-6 else 1.0
        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply pre-computed training scaling parameters to any stream/test split."""
        if not self.is_fitted:
            raise ValueError("Scaler must be fitted on training baseline before transform.")
        scaled_df = df.copy()
        for col in self.feature_cols:
            if col in scaled_df.columns and col in self.means:
                scaled_df[f"{col}_zscore"] = (scaled_df[col] - self.means[col]) / self.stds[col]
        return scaled_df

    def to_dict(self) -> dict:
        """Export scaling parameters for edge deployment and model serving."""
        return {"means": self.means, "stds": self.stds, "feature_cols": self.feature_cols}
