
"""Data cleaning utilities for the HealthSensing AI pipeline."""

import pandas as pd


NUMERIC_COLUMNS = [
    "heart_rate",
    "spo2",
    "body_temperature",
    "activity_level",
    "ambient_temperature",
    "humidity",
    "aqi",
    "pm25",
]


def clean_readings(
    data: pd.DataFrame,
    numeric_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Validate and clean physiological and environmental readings.

    Invalid numeric values are converted to NaN. Rows with invalid
    timestamps are removed. Partially missing sensor readings are
    retained for downstream handling.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if data.empty:
        raise ValueError("Input DataFrame is empty.")

    if "timestamp" not in data.columns:
        raise ValueError("Missing required column: timestamp")

    cleaned = data.copy()

    # Convert timestamps to timezone-aware UTC datetimes.
    cleaned["timestamp"] = pd.to_datetime(
        cleaned["timestamp"],
        errors="coerce",
        utc=True,
    )

    # Remove rows with invalid timestamps.
    cleaned = cleaned.dropna(subset=["timestamp"])

    # Remove completely duplicated records.
    cleaned = cleaned.drop_duplicates()

    columns_to_convert = (
        numeric_columns
        if numeric_columns is not None
        else NUMERIC_COLUMNS
    )

    for column in columns_to_convert:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(
                cleaned[column],
                errors="coerce",
            )

    return cleaned.reset_index(drop=True)
