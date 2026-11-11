"""
Dataset Loaders and Adapters for HealthSensing
Author: Kartikeya Singh (Member 1)
"""
import pandas as pd
import numpy as np
from typing import Union

def load_wesad_data(filepath_or_dict: Union[str, dict]) -> pd.DataFrame:
    """Ingests and standardizes WESAD multimodal wearable data (Empatica E4 signals)."""
    df = pd.read_csv(filepath_or_dict) if isinstance(filepath_or_dict, str) else pd.DataFrame(filepath_or_dict)
    rename_map = {"HR": "heart_rate_bpm", "heart_rate": "heart_rate_bpm", "TEMP": "body_temperature_c", "temp": "body_temperature_c"}
    df = df.rename(columns=rename_map)
    df["source"] = "WESAD"
    for col in ["ambient_temperature_c", "humidity_percent", "aqi", "pm25_ug_m3"]:
        if col not in df.columns:
            df[col] = np.nan
    return df

def load_ljubljana_data(filepath: str) -> pd.DataFrame:
    """Ingests and standardizes Ljubljana Environmental & Biometric dataset."""
    df = pd.read_csv(filepath)
    rename_map = {"PM2.5": "pm25_ug_m3", "Temperature": "ambient_temperature_c", "Humidity": "humidity_percent", "HeartRate": "heart_rate_bpm"}
    df = df.rename(columns=rename_map)
    df["source"] = "Ljubljana"
    for col in ["spo2_percent", "body_temperature_c"]:
        if col not in df.columns:
            df[col] = np.nan
    return df

def load_pixel_watch_export(filepath_or_records: Union[str, list]) -> pd.DataFrame:
    """Ingests Google Takeout / Fitbit JSON exports for personal baseline modeling."""
    df = pd.read_json(filepath_or_records) if isinstance(filepath_or_records, str) else pd.DataFrame(filepath_or_records)
    rename_map = {"bpm": "heart_rate_bpm", "value": "heart_rate_bpm", "dateTime": "timestamp"}
    df = df.rename(columns=rename_map)
    df["source"] = "PixelWatch"
    for col in ["spo2_percent", "body_temperature_c", "ambient_temperature_c", "humidity_percent", "aqi", "pm25_ug_m3"]:
        if col not in df.columns:
            df[col] = np.nan
    return df
