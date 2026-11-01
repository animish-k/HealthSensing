import numpy as np
import pandas as pd
import pytest

from ai.features.baseline_features import extract_baseline_features


@pytest.fixture
def baseline():
    return pd.DataFrame({
        "heart_rate": [72, 74, 73, 75, 71, 74],
        "spo2": [98, 97, 98, 99, 97, 98],
    })


@pytest.fixture
def current():
    return pd.DataFrame({
        "heart_rate": [74, 80, 85, 90],
        "spo2": [98, 97, 96, 95],
    })


def test_baseline_mean(baseline, current):
    result = extract_baseline_features(current, baseline)

    assert result["heart_rate_baseline_mean"].iloc[0] == pytest.approx(
        73.1666667
    )


def test_baseline_standard_deviation(baseline, current):
    result = extract_baseline_features(current, baseline)

    expected = baseline["heart_rate"].std(ddof=1)

    assert result["heart_rate_baseline_std"].iloc[0] == pytest.approx(
        expected
    )


def test_baseline_difference(baseline, current):
    result = extract_baseline_features(current, baseline)

    assert result["heart_rate_baseline_difference"].iloc[0] == pytest.approx(
        74 - baseline["heart_rate"].mean()
    )


def test_baseline_z_score(baseline, current):
    result = extract_baseline_features(current, baseline)

    expected = (
        74 - baseline["heart_rate"].mean()
    ) / baseline["heart_rate"].std(ddof=1)

    assert result["heart_rate_baseline_z_score"].iloc[0] == pytest.approx(
        expected
    )


def test_percentage_deviation(baseline, current):
    result = extract_baseline_features(current, baseline)

    expected = (
        (74 - baseline["heart_rate"].mean())
        / abs(baseline["heart_rate"].mean())
    ) * 100

    assert result[
        "heart_rate_baseline_percentage_deviation"
    ].iloc[0] == pytest.approx(expected)


def test_missing_current_values_are_preserved(baseline):
    readings = pd.DataFrame({
        "heart_rate": [75, np.nan, 80],
    })

    result = extract_baseline_features(
        readings,
        baseline,
        feature_columns=["heart_rate"],
    )

    assert pd.isna(result["heart_rate_baseline_difference"].iloc[1])


def test_requires_two_valid_baseline_values(current):
    baseline_data = pd.DataFrame({
        "heart_rate": [72, np.nan, np.nan],
        "spo2": [98, 97, 98],
    })

    with pytest.raises(ValueError):
        extract_baseline_features(
            current,
            baseline_data,
            feature_columns=["heart_rate"],
        )


def test_missing_columns_raise_error(baseline):
    readings = pd.DataFrame({
        "heart_rate": [75, 80],
    })

    with pytest.raises(ValueError):
        extract_baseline_features(
            readings,
            baseline,
            feature_columns=["spo2"],
        )


def test_zero_variance_baseline_returns_nan_z_score():
    baseline_data = pd.DataFrame({
        "heart_rate": [75, 75, 75, 75],
    })

    readings = pd.DataFrame({
        "heart_rate": [80, 85],
    })

    result = extract_baseline_features(
        readings,
        baseline_data,
    )

    assert result["heart_rate_baseline_z_score"].isna().all()


def test_infinite_values_raise_error(baseline):
    readings = pd.DataFrame({
        "heart_rate": [75, np.inf],
    })

    with pytest.raises(ValueError):
        extract_baseline_features(
            readings,
            baseline,
            feature_columns=["heart_rate"],
        )
