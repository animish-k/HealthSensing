"""
Multimodal Context and Environmental Stress Coupling Module
Author: Kartikeya Singh (Member 1)
"""
import pandas as pd
import numpy as np

def calculate_noaa_heat_index(temp_c: float, humidity: float) -> float:
    """Computes the official NOAA Heat Index (°C) from ambient temperature and relative humidity."""
    if pd.isna(temp_c) or pd.isna(humidity):
        return np.nan
    t_f = (temp_c * 9.0 / 5.0) + 32.0
    r = humidity
    # Rothfusz regression equation for heat index
    hi_f = (-42.379 + 2.04901523 * t_f + 10.14333127 * r - 0.22475541 * t_f * r 
            - 0.00683783 * t_f**2 - 0.05481717 * r**2 + 0.00122874 * t_f**2 * r 
            + 0.00085282 * t_f * r**2 - 0.00000199 * t_f**2 * r**2)
    return round((hi_f - 32.0) * 5.0 / 9.0, 2)

def extract_multimodal_features(df: pd.DataFrame, baseline_hr: float = 72.0) -> pd.DataFrame:
    """
    Extracts cross-domain features for Week 5 ablation evaluation:
    Physiological signals combined with environmental context.
    """
    out = df.copy()
    
    # 1. Scientific Environmental Metric: Heat Index
    if "ambient_temperature_c" in out.columns and "humidity_percent" in out.columns:
        out["heat_index_c"] = [
            calculate_noaa_heat_index(t, h) 
            for t, h in zip(out["ambient_temperature_c"], out["humidity_percent"])
        ]
    
    # 2. Environmental-Physiological Interaction: Thermal Strain Ratio
    if "heart_rate_bpm" in out.columns and "ambient_temperature_c" in out.columns:
        out["thermal_strain_index"] = (out["heart_rate_bpm"] / baseline_hr) * (out["ambient_temperature_c"] / 25.0)
    
    # 3. Respiratory Risk Metric: Pollution Exposure Rate (AQI combined with activity exertion)
    if "aqi" in out.columns:
        activity_multiplier = {"sedentary": 1.0, "walking": 2.0, "running": 4.0}
        mult = out["activity_level"].map(activity_multiplier).fillna(1.0) if "activity_level" in out.columns else 1.0
        out["pollution_exposure_rate"] = out["aqi"] * mult

    return out
