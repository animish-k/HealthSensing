
"""
HealthSensing: Personal baseline anomaly detector.

This module flags readings that deviate from a reference baseline.
It is an experimental anomaly detector, not a medical diagnostic tool.
"""

from collections.abc import Sequence

import numpy as np
import pandas as pd


def detect_anomalies(
    readings: Sequence[float],
    baseline_readings: Sequence[float],
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Flag readings that deviate from a personal reference baseline.

    Args:
        readings: Heart-rate measurements to evaluate, in bpm.
        baseline_readings: Reference measurements representing the
            individual's baseline period.
        threshold: Absolute z-score above which to flag a reading.

    Returns:
        DataFrame containing heart rate, z-score, and anomaly flag.

    Note:
        The baseline should be selected independently of the readings
        being evaluated. Thresholds require validation for the intended
        application and are not medically validated.
    """
    values = np.asarray(readings, dtype=float)
    baseline = np.asarray(baseline_readings, dtype=float)

    if values.ndim != 1 or baseline.ndim != 1:
        raise ValueError("Readings must be one-dimensional.")

    if len(values) == 0 or len(baseline) < 2:
        raise ValueError(
            "Provide readings and at least two baseline measurements."
        )

    if not np.isfinite(values).all():
        raise ValueError("Readings must contain only finite values.")

    if not np.isfinite(baseline).all():
        raise ValueError("Baseline must contain only finite values.")

    if not np.isfinite(threshold) or threshold <= 0:
        raise ValueError("Threshold must be a positive finite number.")

    baseline_mean = float(np.mean(baseline))
    baseline_std = float(np.std(baseline, ddof=1))

    if baseline_std == 0:
        raise ValueError(
            "Baseline has zero variation; z-scores are undefined."
        )

    z_scores = (values - baseline_mean) / baseline_std

    return pd.DataFrame({
        "heart_rate_bpm": values,
        "z_score": z_scores,
        "detected_anomaly": (
            np.abs(z_scores) > threshold
        ).astype(int),
    })
