
"""Normalization utilities for the HealthSensing AI pipeline."""

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler


class DataFrameNormalizer:
    """
    Normalize numerical columns while preserving non-numerical columns.

    Supported methods:
        - standard: StandardScaler (mean 0, standard deviation 1)
        - minmax: MinMaxScaler (default range 0 to 1)

    Fit the normalizer on training data only. Reuse the fitted
    normalizer to transform validation and test data.
    """

    def __init__(
        self,
        method: str = "standard",
        feature_range: tuple[float, float] = (0, 1),
    ):
        if method not in ("standard", "minmax"):
            raise ValueError(
                "Method must be 'standard' or 'minmax'."
            )

        self.method = method
        self.feature_range = feature_range
        self.scaler = None
        self.columns = None
        self.fitted = False

    def fit(self, data: pd.DataFrame):
        """Learn scaling parameters from training data."""

        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        if data.empty:
            raise ValueError("Input DataFrame is empty.")

        self.columns = data.select_dtypes(
            include=[np.number]
        ).columns.tolist()

        if not self.columns:
            raise ValueError("No numerical columns found.")

        numeric_data = data[self.columns]

        if np.isinf(numeric_data.to_numpy(dtype=float)).any():
            raise ValueError("Data must not contain infinite values.")

        if self.method == "standard":
            self.scaler = StandardScaler()
        else:
            self.scaler = MinMaxScaler(
                feature_range=self.feature_range
            )

        self.scaler.fit(numeric_data)
        self.fitted = True

        return self

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data using previously learned parameters."""

        if not self.fitted:
            raise RuntimeError(
                "Normalizer has not been fitted. Call fit() first."
            )

        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        if not data.columns.is_unique:
            raise ValueError("DataFrame columns must be unique.")

        missing_columns = [
            col for col in self.columns if col not in data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing numerical columns: {missing_columns}"
            )

        numeric_data = data[self.columns]

        if np.isinf(numeric_data.to_numpy(dtype=float)).any():
            raise ValueError("Data must not contain infinite values.")

        result = data.copy()
        result[self.columns] = self.scaler.transform(numeric_data)

        return result

    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Fit on data and return its normalized version."""

        return self.fit(data).transform(data)
