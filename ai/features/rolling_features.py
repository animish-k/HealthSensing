
"""Rolling statistical features for HealthSensing."""

import numpy as np
import pandas as pd


def calculate_rolling_features(
    data: pd.DataFrame,
    feature_columns: list[str] | None = None,
    window_size: int = 3,
    min_periods: int | None = None,
) -> pd.DataFrame:
    """
    Calculate rolling statistics for selected numerical columns.

    Features generated:
        - rolling_mean
        - rolling_std
        - rolling_min
        - rolling_max
        - rolling_range

    Args:
        data: Input time-series DataFrame.
        feature_columns: Numerical columns to process.
        window_size: Number of consecutive readings per window.
        min_periods: Minimum observations required to calculate
            a statistic. Defaults to window_size.

    Returns:
        A copy of the input DataFrame with rolling feature columns.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if data.empty:
        raise ValueError("Input DataFrame is empty.")

    if not isinstance(window_size, int) or isinstance(window_size, bool):
        raise TypeError("window_size must be an integer.")

    if window_size <= 0:
        raise ValueError("window_size must be positive.")

    if min_periods is None:
        min_periods = window_size

    if (
        not isinstance(min_periods, int)
        or isinstance(min_periods, bool)
    ):
        raise TypeError("min_periods must be an integer.")

    if min_periods <= 0 or min_periods > window_size:
        raise ValueError(
            "min_periods must be between 1 and window_size."
        )

    if feature_columns is None:
        feature_columns = data.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    if not feature_columns:
        raise ValueError("No numerical feature columns found.")

    missing_columns = [
        col for col in feature_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing feature columns: {missing_columns}"
        )

    result = data.copy()

    for column in feature_columns:
        values = pd.to_numeric(
            result[column],
            errors="coerce",
        )

        if np.isinf(values.to_numpy(dtype=float)).any():
            raise ValueError(
                f"Column '{column}' contains infinite values."
            )

        rolling = values.rolling(
            window=window_size,
            min_periods=min_periods,
        )

        result[f"{column}_rolling_mean"] = rolling.mean()
        result[f"{column}_rolling_std"] = rolling.std()
        result[f"{column}_rolling_min"] = rolling.min()
        result[f"{column}_rolling_max"] = rolling.max()

        result[f"{column}_rolling_range"] = (
            rolling.max() - rolling.min()
        )

    return result
