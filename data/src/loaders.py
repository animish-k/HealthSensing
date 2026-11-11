import pandas as pd
import numpy as np

def load_wesad_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    rename_map = {"HR": "heart_rate_bpm", "TEMP": "body_temperature_c", "EDA": "eda_microsiemens", "label": "stress_label"}
    df = df.rename(columns=rename_map)
    df["source"] = "WESAD"
    if "participant_id" not in df.columns:
        df["participant_id"] = "S2"
    if "session_id" not in df.columns:
        df["session_id"] = "WESAD_S2"
    return df

def load_ljubljana_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    rename_map = {"PM2.5": "pm25_ug_m3", "Temperature": "ambient_temperature_c", "Humidity": "humidity_percent", "HeartRate": "heart_rate_bpm"}
    df = df.rename(columns=rename_map)
    df["source"] = "Ljubljana"
    if "participant_id" not in df.columns:
        df["participant_id"] = "VOL_01"
    if "session_id" not in df.columns:
        df["session_id"] = "LJ_01"
    return df
