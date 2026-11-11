"""
Comprehensive Preprocessing Pipeline Test Suite
Author: Kartikeya Singh (Member 1)
Tests: Missing Data, Duplicate Timestamps, Outlier Spikes, and Normalization
"""
import pandas as pd
import numpy as np
from data.src.cleaner import clean_dataframe, clean_record
from data.src.features import extract_window_features, summarize_personal_baseline
from data.src.scaler import LeakageSafeScaler

def test_1_missing_data_resilience():
    """Verify missing/null sensor data does not crash pipeline and is preserved as NaN."""
    df_missing = pd.DataFrame([
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 72.0, "eda_microsiemens": None, "ambient_temperature_c": None},
        {"timestamp": "2026-11-11T10:01:00Z", "heart_rate_bpm": 74.0, "eda_microsiemens": None, "ambient_temperature_c": None}
    ])
    cleaned = clean_dataframe(df_missing)
    features = extract_window_features(cleaned, window_size=2)
    assert pd.isna(features.loc[0, "ambient_temperature_c_rolling_mean"]), "Missing signals must produce NaN, not 0"
    print(" [PASS] Test 1: Missing and null data handled safely without imputation bias.")

def test_2_duplicate_and_out_of_order_timestamps():
    """Verify duplicate timestamps are resolved and unordered records sorted chronologically."""
    df_duplicates = pd.DataFrame([
        {"timestamp": "2026-11-11T10:02:00Z", "heart_rate_bpm": 80.0},
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 70.0}, # Out-of-order
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 71.0}  # Duplicate timestamp
    ])
    cleaned = clean_dataframe(df_duplicates)
    assert len(cleaned) == 2, "Duplicate timestamp must be deduplicated"
    assert cleaned.loc[0, "heart_rate_bpm"] == 71.0, "Sorted chronologically, keeping latest reading"
    print(" [PASS] Test 2: Duplicate timestamps resolved and chronological order restored.")

def test_3_physiological_outlier_filtering():
    """Verify impossible sensor glitches (e.g. HR=350 bpm, SpO2=30%) are nullified."""
    df_spikes = pd.DataFrame([
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 350.0, "spo2_percent": 30.0},
        {"timestamp": "2026-11-11T10:01:00Z", "heart_rate_bpm": 75.0, "spo2_percent": 98.0}
    ])
    cleaned = clean_dataframe(df_spikes)
    assert pd.isna(cleaned.loc[0, "heart_rate_bpm"]), "Extreme HR > 220 bpm must be replaced with NaN"
    assert pd.isna(cleaned.loc[0, "spo2_percent"]), "SpO2 < 70% must be replaced with NaN"
    assert cleaned.loc[1, "heart_rate_bpm"] == 75.0, "Valid vital reading preserved"
    print(" [PASS] Test 3: Physiological sensor outlier spikes filtered out.")

def test_4_leakage_safe_normalization():
    """Verify Z-score normalizer parameters are fitted exclusively on training baseline split."""
    # Training baseline: mean = 70.0, std = 10.0
    baseline_train = pd.DataFrame({"heart_rate_bpm": [60.0, 70.0, 80.0]})
    # Future unseen test observation
    test_stream = pd.DataFrame({"heart_rate_bpm": [90.0]})
    
    scaler = LeakageSafeScaler(["heart_rate_bpm"]).fit(baseline_train)
    transformed = scaler.transform(test_stream)
    
    expected_zscore = (90.0 - 70.0) / 10.0 # Exactly +2.0 std deviations above baseline
    assert abs(transformed.loc[0, "heart_rate_bpm_zscore"] - expected_zscore) < 1e-2
    print(" [PASS] Test 4: Leakage-safe normalization verified (fitted strictly on baseline).")

if __name__ == "__main__":
    print("=" * 65)
    print("Running Member 1 Data Preprocessing Test Suite")
    print("=" * 65)
    test_1_missing_data_resilience()
    test_2_duplicate_and_out_of_order_timestamps()
    test_3_physiological_outlier_filtering()
    test_4_leakage_safe_normalization()
    print("\n[SUCCESS] ALL PREPROCESSING TESTS PASSED (100% VERIFIED)!")
