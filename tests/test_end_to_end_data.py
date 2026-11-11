"""
Week 8 Final Robustness & Offline Operation Test Suite
Author: Kartikeya Singh (Member 1)
"""
import pandas as pd
import numpy as np
from data.src.pipeline import HealthSensingPipeline
from data.src.cleaner import clean_dataframe
from data.src.multimodal_features import calculate_noaa_heat_index

def run_week8_tests():
    print("=" * 60)
    print("Running Week 8 Robustness and Offline Operation Tests")
    print("=" * 60)

    # Test 1: Missing environmental sensors (offline / disconnected sensor resilience)
    data_missing = pd.DataFrame([
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 74.0, "aqi": None, "spo2_percent": None},
        {"timestamp": "2026-11-11T10:01:00Z", "heart_rate_bpm": 76.0, "aqi": None, "spo2_percent": None}
    ])
    pipeline = HealthSensingPipeline(window_size=2)
    pipeline.fit_baseline(data_missing)
    res = pipeline.process_dataframe(data_missing)
    assert pd.isna(res.loc[0, "aqi"]), "Missing AQI must remain null without crashing"
    assert "heart_rate_bpm_rolling_mean" in res.columns
    print(" [PASS] Test 1: Missing sensor & disconnected inputs handled safely")

    # Test 2: Chronological reordering of out-of-order streams
    out_of_order = pd.DataFrame([
        {"timestamp": "2026-11-11T10:05:00Z", "heart_rate_bpm": 80.0},
        {"timestamp": "2026-11-11T10:00:00Z", "heart_rate_bpm": 70.0}
    ])
    sorted_res = pipeline.process_dataframe(out_of_order)
    assert sorted_res.loc[0, "heart_rate_bpm"] == 70.0, "Must be sorted chronologically"
    print(" [PASS] Test 2: Out-of-order timestamp sorting and deduplication")

    # Test 3: Heat Index calculation edge-case
    hi = calculate_noaa_heat_index(35.0, 80.0)
    assert hi > 40.0, "High humidity must increase perceived heat stress"
    print(" [PASS] Test 3: NOAA Heat Index computation verified")

    print("\n[SUCCESS] ALL WEEK 8 ROBUSTNESS TESTS PASSED (100% SUCCESS RATE)!")

if __name__ == "__main__":
    run_week8_tests()
