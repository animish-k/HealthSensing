
import numpy as np
import pytest

from ai.baseline.personal_baseline import detect_anomalies


def test_detects_high_and_low_deviations():
    baseline = [70, 72, 71, 69, 70, 71, 72, 70]
    readings = [70, 71, 100, 40]

    result = detect_anomalies(
        readings,
        baseline,
        threshold=2.0,
    )

    assert result["detected_anomaly"].tolist() == [0, 0, 1, 1]


def test_returns_expected_columns():
    result = detect_anomalies(
        readings=[70, 71],
        baseline_readings=[69, 70, 71, 72],
    )

    assert list(result.columns) == [
        "heart_rate_bpm",
        "z_score",
        "detected_anomaly",
    ]


def test_rejects_insufficient_baseline():
    with pytest.raises(ValueError):
        detect_anomalies([70], [70])


def test_rejects_zero_variation_baseline():
    with pytest.raises(ValueError):
        detect_anomalies([75], [70, 70, 70])


def test_rejects_non_finite_readings():
    with pytest.raises(ValueError):
        detect_anomalies([70, np.nan], [69, 70, 71])


def test_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        detect_anomalies([70], [69, 70, 71], threshold=0)
