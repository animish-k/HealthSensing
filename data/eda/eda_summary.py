import json
import pandas as pd
from data.src.cleaner import clean_dataframe
from data.src.features import extract_window_features, summarize_personal_baseline

def main():
    print("Testing pipeline with sample data...")
    with open("data/samples/sample_processed.json", "r") as f:
        records = json.load(f)
    df = clean_dataframe(pd.DataFrame(records))
    baseline = summarize_personal_baseline(df)
    features = extract_window_features(df, window_size=2, baseline_stats=baseline)
    print("\nExtracted features preview:")
    print(features[["timestamp", "heart_rate_bpm", "heart_rate_bpm_rolling_mean", "heart_rate_bpm_dev_from_baseline"]])

if __name__ == "__main__":
    main()
