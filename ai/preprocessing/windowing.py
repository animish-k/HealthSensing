
"""Time-series windowing utilities for the HealthSensing AI pipeline."""

import pandas as pd


def create_windows(
    data: pd.DataFrame,
    window_size: int,
    stride: int = 1,
    timestamp_column: str = "timestamp",
) -> list[pd.DataFrame]:
    """
    Divide time-series readings into chronological windows.

    Args:
        data: Input DataFrame containing sensor readings.
        window_size: Number of readings in each window.
        stride: Number of readings to advance between windows.
        timestamp_column: Column used to sort readings chronologically.

    Returns:
        List of DataFrames, each containing one complete window.

    Note:
        Incomplete windows at the end are discarded.
        Original row indices are reset in each returned window.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if data.empty:
        raise ValueError("Input DataFrame is empty.")

    if not isinstance(window_size, int) or isinstance(window_size, bool):
        raise TypeError("window_size must be an integer.")

    if not isinstance(stride, int) or isinstance(stride, bool):
        raise TypeError("stride must be an integer.")

    if window_size <= 0:
        raise ValueError("window_size must be positive.")

    if stride <= 0:
        raise ValueError("stride must be positive.")

    if timestamp_column not in data.columns:
        raise ValueError(
            f"Missing timestamp column: {timestamp_column}"
        )

    if data[timestamp_column].isna().any():
        raise ValueError("Timestamp column contains missing values.")

    result = data.copy()

    result[timestamp_column] = pd.to_datetime(
        result[timestamp_column],
        errors="coerce",
        utc=True,
    )

    if result[timestamp_column].isna().any():
        raise ValueError("Timestamp column contains invalid values.")

    result = result.sort_values(
        timestamp_column
    ).reset_index(drop=True)

    windows = []

    for start in range(0, len(result) - window_size + 1, stride):
        end = start + window_size

        window = result.iloc[start:end].copy()
        window = window.reset_index(drop=True)

        windows.append(window)

    return windows
