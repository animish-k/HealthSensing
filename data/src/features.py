import pandas as pd
import numpy as np

def extract_window_features(df: pd.DataFrame, window_size: int = 5, baseline_stats: dict = None) -> pd.DataFrame:
    """Computes rolling statistics, deltas, and baseline deviations safely even with missing/None sensors."""
    df = df.copy()
    signals = [c for c in ["heart_rate_bpm", "spo2_percent", "ambient_temperature_c", "pm25_ug_m3", "aqi"] if c in df.columns]
    
    for col in signals:
        # Safely convert to numeric float, turning None into NaN
        s = pd.to_numeric(df[col], errors='coerce')
        
        # If the sensor was completely disconnected/empty, safely fill NaN
        if s.dropna().count() == 0:
            df[f"{col}_rolling_mean"] = np.nan
            df[f"{col}_rolling_std"] = np.nan
            df[f"{col}_delta"] = np.nan
            continue
            
        df[f"{col}_rolling_mean"] = s.rolling(window=window_size, min_periods=1).mean().round(2)
        df[f"{col}_rolling_std"] = s.rolling(window=window_size, min_periods=1).std().fillna(0.0).round(2)
        df[f"{col}_delta"] = s.diff().fillna(0.0).round(2)
        
        if baseline_stats and col in baseline_stats:
            mean_base = baseline_stats[col].get("mean", s.mean())
            if pd.notna(mean_base):
                df[f"{col}_dev_from_baseline"] = (s - mean_base).round(2)
    return df

def summarize_personal_baseline(df: pd.DataFrame) -> dict:
    """Computes summary statistics for personal baseline."""
    baseline = {}
    for col in ["heart_rate_bpm", "spo2_percent", "body_temperature_c"]:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors='coerce').dropna()
            if len(s) > 0:
                baseline[col] = {
                    "mean": round(float(s.mean()), 2),
                    "std": round(float(s.std()), 2)
                }
    return baseline
