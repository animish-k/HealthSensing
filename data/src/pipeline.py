"""
Unified Pipeline for Week 7 Backend Integration
Author: Kartikeya Singh (Member 1)
"""
import pandas as pd
from data.src.cleaner import clean_dataframe, clean_record
from data.src.features import extract_window_features, summarize_personal_baseline
from data.src.multimodal_features import extract_multimodal_features
from data.src.scaler import LeakageSafeScaler

class HealthSensingPipeline:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.scaler = LeakageSafeScaler()
        self.baseline_stats = {}

    def fit_baseline(self, baseline_df: pd.DataFrame):
        cleaned = clean_dataframe(baseline_df)
        self.baseline_stats = summarize_personal_baseline(cleaned)
        self.scaler.fit(cleaned)
        return self

    def process_record(self, raw_record: dict) -> dict:
        """FastAPI helper: processes a single incoming streaming reading."""
        cleaned = clean_record(raw_record)
        return cleaned

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """AI & Batch helper: processes a time-series window."""
        cleaned = clean_dataframe(df)
        windowed = extract_window_features(cleaned, window_size=self.window_size, baseline_stats=self.baseline_stats)
        b_hr = self.baseline_stats.get("heart_rate_bpm", {}).get("mean", 72.0)
        multimodal = extract_multimodal_features(windowed, baseline_hr=b_hr)
        scaled = self.scaler.transform(multimodal) if self.scaler.is_fitted else multimodal
        return scaled
