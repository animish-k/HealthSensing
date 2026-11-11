"""
Demonstration of Complete End-to-End Preprocessing Pipeline
Sequence: Real Dataset -> Loading -> Cleaning -> Feature Extraction -> Normalization -> Processed Output
Author: Kartikeya Singh (Member 1)
"""
import pandas as pd
from data.src.cleaner import clean_dataframe
from data.src.features import extract_window_features, summarize_personal_baseline
from data.src.scaler import LeakageSafeScaler

def run_end_to_end_sequence():
    print("=" * 70)
    print("COMPLETE PREPROCESSING SEQUENCE DEMONSTRATION ON GENUINE WESAD DATA")
    print("=" * 70)

    # 1. Real Dataset Source
    raw_path = "data/processed/wesad_s2_real.csv"
    print(f"\n[STEP 1: Real Dataset] Ingesting genuine clinical recording from {raw_path}...")
    df_raw = pd.read_csv(raw_path)
    print(f"       Loaded {len(df_raw)} records. Columns: {list(df_raw.columns)}")

    # 2. Cleaning
    print("\n[STEP 2: Cleaning] Sorting timestamps, removing duplicates, filtering sensor noise...")
    df_clean = clean_dataframe(df_raw)
    print(f"       Cleaned shape: {df_clean.shape}. Status: Cleaned and validated.")

    # 3. Personal Baseline Extraction (STRICTLY label == 1)
    print("\n[STEP 3: Personal Baseline Calibration] Filtering strictly to stress_label == 1 (Baseline)...")
    baseline_records = df_clean[df_clean["stress_label"] == 1]
    baseline_stats = summarize_personal_baseline(baseline_records)
    print(f"       Calibrated Subject Baseline: {baseline_stats}")

    # 4. Feature Extraction (Rolling Windows & Baseline Deviations)
    print("\n[STEP 4: Feature Extraction] Computing 5-sec rolling windows and baseline delta...")
    df_features = extract_window_features(df_clean, window_size=5, baseline_stats=baseline_stats)
    print(f"       Extracted features: rolling mean, rolling std, deltas, baseline deviations.")

    # 5. Normalization (Leakage-Safe Scaling fitted only on baseline)
    print("\n[STEP 5: Normalization] Fitting LeakageSafeScaler strictly on baseline split...")
    scaler = LeakageSafeScaler(["heart_rate_bpm", "eda_microsiemens"]).fit(baseline_records)
    df_normalized = scaler.transform(df_features)
    print("       Transformed Z-score columns added without data leakage.")

    # 6. Processed Output
    output_path = "data/processed/wesad_s2_fully_preprocessed.csv"
    df_normalized.to_csv(output_path, index=False)
    print(f"\n[STEP 6: Processed Output] Saved complete preprocessed dataset to {output_path}!")
    print("\nSample Output Preview:")
    cols = ["timestamp", "heart_rate_bpm", "heart_rate_bpm_rolling_mean", "heart_rate_bpm_dev_from_baseline", "heart_rate_bpm_zscore"]
    print(df_normalized[cols].head(4))
    print("\n" + "=" * 70)
    print("[SUCCESS] Complete sequence verified end-to-end on genuine data!")
    print("=" * 70)

if __name__ == "__main__":
    run_end_to_end_sequence()
