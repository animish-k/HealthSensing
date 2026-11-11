"""
Automated Unit Tests for Member 1 Data Pipeline
Author: Kartikeya Singh (Member 1)
"""
import pytest
import pandas as pd
import numpy as np
from data.src.cleaner import clean_dataframe
from data.src.features import extract_window_features
from data.src.scaler import LeakageSafeScaler
from data.src.multimodal_features import calculate_noaa_heat_index

def test_sensor_spike_cleaning():
    """Verify that impossible sensor values are nullified rather than accepted."""
    dirty_data = pd.DataFrame([
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 350.0}, # Impossible HR spike
        {"timestamp": "2026-11-11T10:01:00Z", "heart_rate_bpm": 72.0}
    ])
    cleaned = clean_dataframe(dirty_data)
    assert pd.isna(cleaned.loc[0, "heart_rate_bpm"]), "Spike above 220 bpm must be replaced with NaN"
    assert cleaned.loc[1, "heart_rate_bpm"] == 72.0

def test_leakage_safe_scaling():
    """Verify that scaler parameters come exclusively from baseline training data."""
    train_df = pd.DataFrame({"heart_rate_bpm": [60.0, 80.0]}) # Mean: 70.0, Std: ~14.14
    test_df = pd.DataFrame({"heart_rate_bpm": [70.0]})
    scaler = LeakageSafeScaler(["heart_rate_bpm"]).fit(train_df)
    transformed = scaler.transform(test_df)
    assert abs(transformed.loc[0, "heart_rate_bpm_zscore"]) < 1e-3, "Z-score for training mean must be 0"

def test_heat_index_calculation():
    """Verify NOAA Heat Index calculation."""
    hi = calculate_noaa_heat_index(temp_c=32.0, humidity=70.0)
    assert hi > 35.0, "High humidity must increase perceived heat index"
    print("\nAll unit tests passed successfully!")

if __name__ == "__main__":
    test_sensor_spike_cleaning()
    test_leakage_safe_scaling()
    test_heat_index_calculation()
