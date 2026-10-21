
"""Reproducible evaluation of the HealthSensing personal baseline detector.

This script generates a synthetic demonstration dataset, fits the detector
on an initial reference period, and evaluates subsequent readings.

It does not measure real-world or medical performance.
"""

import numpy as np
import pandas as pd
import sys
from pathlib import path
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ai.baseline.personal_baseline import detect_anomalies


def make_synthetic_data(seed: int = 42) -> pd.DataFrame:
    """Generate reproducible heart-rate readings with injected anomalies."""
    rng = np.random.default_rng(seed)
    n = 600

    timestamps = pd.date_range(
        "2026-01-01 08:00:00",
        periods=n,
        freq="min",
    )

    heart_rate = rng.normal(loc=75.0, scale=2.5, size=n)
    labels = np.zeros(n, dtype=int)

    # Inject a gradual rise after the baseline period.
    heart_rate[300:360] = np.linspace(80, 95, 60) + rng.normal(
        0, 1.5, size=60
    )
    labels[300:360] = 1

    # Inject a sharp spike.
    heart_rate[420:430] = rng.normal(loc=105, scale=3, size=10)
    labels[420:430] = 1

    return pd.DataFrame({
        "timestamp": timestamps,
        "heart_rate_bpm": heart_rate,
        "injected_anomaly": labels,
    })


def evaluate(seed: int = 42, baseline_size: int = 120) -> None:
    """Evaluate on readings that occur after the baseline period."""
    df = make_synthetic_data(seed)

    baseline = df["heart_rate_bpm"].iloc[:baseline_size].to_numpy()
    test_df = df.iloc[baseline_size:].copy()

    predictions = detect_anomalies(
        readings=test_df["heart_rate_bpm"].to_numpy(),
        baseline_readings=baseline,
        threshold=3.0,
    )["detected_anomaly"].to_numpy()

    truth = test_df["injected_anomaly"].to_numpy()

    print("SYNTHETIC HELD-OUT-TIME EVALUATION")
    print(f"Seed: {seed}")
    print(f"Baseline readings: {baseline_size}")
    print(f"Evaluation readings: {len(test_df)}")
    print(f"Precision: {precision_score(truth, predictions, zero_division=0):.3f}")
    print(f"Recall:    {recall_score(truth, predictions, zero_division=0):.3f}")
    print(f"F1-score:  {f1_score(truth, predictions, zero_division=0):.3f}")
    print("Confusion matrix:")
    print(confusion_matrix(truth, predictions, labels=[0, 1]))


if __name__ == "__main__":
    evaluate()
