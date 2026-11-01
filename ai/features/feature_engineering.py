
"""Statistical feature extraction for HealthSensing."""

import numpy as np
import pandas as pd


def extract_window_features(
    window: pd.DataFrame,
    feature_columns: list[str] | None = None,
    timestamp_column: str = "timestamp",
) -> dict:
    """
    Extract statistical features from a single time-series window.

    For each selected numerical column, calculate:
        - Mean
        - Standard deviation
        - Minimum
        - Maximum
        - Range
        - Linear trend (slope)

    Missing values are ignored in statistical calculations.
    Trend is calculated using available finite observations.
    """

    if not isinstance(window, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if window.empty:
        raise ValueError("Input window is empty.")

    if feature_columns is None:
        feature_columns = window.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    if not feature_columns:
        raise ValueError("No numerical feature columns provided.")

    missing_columns = [
        col for col in feature_columns
        if col not in window.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing feature columns: {missing_columns}"
        )

    features = {}

    for column in feature_columns:
        values = pd.to_numeric(
            window[column],
            errors="coerce",
        ).to_numpy(dtype=float)

        finite_mask = np.isfinite(values)
        valid_values = values[finite_mask]

        prefix = column

        if len(valid_values) == 0:
            features[f"{prefix}_mean"] = np.nan
            features[f"{prefix}_std"] = np.nan
            features[f"{prefix}_min"] = np.nan
            features[f"{prefix}_max"] = np.nan
            features[f"{prefix}_range"] = np.nan
            features[f"{prefix}_trend"] = np.nan
            continue

        features[f"{prefix}_mean"] = float(
            np.mean(valid_values)
        )

        features[f"{prefix}_std"] = float(
            np.std(valid_values, ddof=1)
        ) if len(valid_values) >= 2 else np.nan

        features[f"{prefix}_min"] = float(
            np.min(valid_values)
        )

        features[f"{prefix}_max"] = float(
            np.max(valid_values)
        )

        features[f"{prefix}_range"] = float(
            np.max(valid_values) - np.min(valid_values)
        )

        if len(valid_values) >= 2:
            positions = np.flatnonzero(finite_mask)

            features[f"{prefix}_trend"] = float(
                np.polyfit(positions, valid_values, 1)[0]
            )
        else:
            features[f"{prefix}_trend"] = np.nan

    return features


def extract_features_from_windows(
    windows: list[pd.DataFrame],
    feature_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Extract one feature row for every input window."""

    if not isinstance(windows, list):
        raise TypeError("Windows must be provided as a list.")

    if not windows:
        raise ValueError("At least one window is required.")

    extracted = [
        extract_window_features(
            window,
            feature_columns=feature_columns,
        )
        for window in windows
    ]

    return pd.DataFrame(extracted)
