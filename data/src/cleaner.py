import pandas as pd
import numpy as np
from typing import Dict, Any

VALID_RANGES = {
    "heart_rate_bpm": (30.0, 220.0),
    "spo2_percent": (70.0, 100.0),
    "body_temperature_c": (34.0, 43.0),
    "ambient_temperature_c": (-20.0, 55.0),
    "humidity_percent": (0.0, 100.0),
    "aqi": (0.0, 500.0),
    "pm25_ug_m3": (0.0, 1000.0)
}

def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Validates and cleans a single streaming dictionary record."""
    cleaned = record.copy()
    for col, (low, high) in VALID_RANGES.items():
        if col in cleaned and cleaned[col] is not None:
            try:
                val = float(cleaned[col])
                if val < low or val > high:
                    cleaned[col] = None
                else:
                    cleaned[col] = val
            except (ValueError, TypeError):
                cleaned[col] = None
    return cleaned

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts timestamps, drops duplicates, and nullifies sensor glitches."""
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"], keep="last").reset_index(drop=True)
    
    for col, (low, high) in VALID_RANGES.items():
        if col in df.columns:
            mask = (df[col] < low) | (df[col] > high)
            df.loc[mask, col] = np.nan
    return df
