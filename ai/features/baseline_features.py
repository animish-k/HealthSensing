
"""Personal baseline feature extraction for HealthSensing."""

import numpy as np
import pandas as pd


def extract_baseline_features(
    readings: pd.DataFrame,
    baseline_readings: pd.DataFrame,
    feature_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Calculate deviations from an individual's reference baseline.

    For each selected numerical feature, calculate:
        - baseline_mean
        - baseline_std
        - baseline_difference
        - baseline_z_score
        - baseline_percentage_deviation

    Baseline statistics are calculated only from baseline_readings.

    Parameters
    ----------
    readings : pd.DataFrame
        Current sensor readings.
    baseline_readings : pd.DataFrame
        Historical readings used to calculate personal baseline statistics.
    feature_columns : list[str] | None
        Numerical columns to process. If None, numerical columns
        from readings are selected automatically.

    Returns
    -------
    pd.DataFrame
        Original readings with additional baseline-derived features.

    Notes
    -----
    This is an experimental feature extraction component.
    It is not medically validated and must not be used for diagnosis.
    """

    if not isinstance(readings, pd.DataFrame):
        raise TypeError("Readings must be a pandas DataFrame.")

    if not isinstance(baseline_readings, pd.DataFrame):
        raise TypeError("Baseline readings must be a pandas DataFrame.")

    if readings.empty:
        raise ValueError("Readings DataFrame is empty.")

    if baseline_readings.empty:
        raise ValueError("Baseline DataFrame is empty.")

    if feature_columns is None:
        feature_columns = readings.select_dtypes(
            include=[np.number]
        ).columns.tolist()

    if not feature_columns:
        raise ValueError("No numerical feature columns found.")

    missing_reading_columns = [
        col for col in feature_columns
        if col not in readings.columns
    ]

    missing_baseline_columns = [
        col for col in feature_columns
        if col not in baseline_readings.columns
    ]

    if missing_reading_columns or missing_baseline_columns:
        raise ValueError(
            "Missing columns. "
            f"Readings: {missing_reading_columns}; "
            f"Baseline: {missing_baseline_columns}"
        )

    result = readings.copy()

    for column in feature_columns:
        current = pd.to_numeric(
            readings[column],
            errors="coerce",
        )

        baseline = pd.to_numeric(
            baseline_readings[column],
            errors="coerce",
        )

        current_values = current.to_numpy(dtype=float)
        baseline_values = baseline.to_numpy(dtype=float)

        if np.isinf(current_values).any():
            raise ValueError(
                f"Readings column '{column}' contains infinite values."
            )

        if np.isinf(baseline_values).any():
            raise ValueError(
                f"Baseline column '{column}' contains infinite values."
            )

        valid_baseline = baseline.dropna()

        if len(valid_baseline) < 2:
            raise ValueError(
                f"At least two valid baseline values are required "
                f"for '{column}'."
            )

        baseline_mean = float(valid_baseline.mean())
        baseline_std = float(valid_baseline.std(ddof=1))

        result[f"{column}_baseline_mean"] = baseline_mean
        result[f"{column}_baseline_std"] = baseline_std

        result[f"{column}_baseline_difference"] = (
            current - baseline_mean
        )

        if baseline_std == 0:
            result[f"{column}_baseline_z_score"] = np.nan
        else:
            result[f"{column}_baseline_z_score"] = (
                (current - baseline_mean) / baseline_std
            )

        if baseline_mean == 0:
            result[
                f"{column}_baseline_percentage_deviation"
            ] = np.nan
        else:
            result[
                f"{column}_baseline_percentage_deviation"
            ] = (
                (current - baseline_mean)
                / abs(baseline_mean)
            ) * 100

    return result
