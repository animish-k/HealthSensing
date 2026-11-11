import pandas as pd

def extract_window_features(df: pd.DataFrame, window_size: int = 5, baseline_stats: dict = None) -> pd.DataFrame:
    """Computes rolling statistics, deltas, and baseline deviations."""
    df = df.copy()
    signals = [c for c in ["heart_rate_bpm", "spo2_percent", "ambient_temperature_c", "pm25_ug_m3", "aqi"] if c in df.columns]
    
    for col in signals:
        df[f"{col}_rolling_mean"] = df[col].rolling(window=window_size, min_periods=1).mean().round(2)
        df[f"{col}_rolling_std"] = df[col].rolling(window=window_size, min_periods=1).std().fillna(0.0).round(2)
        df[f"{col}_delta"] = df[col].diff().fillna(0.0).round(2)
        
        if baseline_stats and col in baseline_stats:
            mean_base = baseline_stats[col].get("mean", df[col].mean())
            df[f"{col}_dev_from_baseline"] = (df[col] - mean_base).round(2)
    return df

def summarize_personal_baseline(df: pd.DataFrame) -> dict:
    """Computes summary statistics for personal baseline."""
    baseline = {}
    for col in ["heart_rate_bpm", "spo2_percent", "body_temperature_c"]:
        if col in df.columns and df[col].dropna().count() > 0:
            baseline[col] = {
                "mean": round(float(df[col].mean()), 2),
                "std": round(float(df[col].std()), 2)
            }
    return baseline
