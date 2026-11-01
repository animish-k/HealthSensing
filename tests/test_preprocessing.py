


import pandas as pd
import pytest

from ai.preprocessing.cleaning import clean_readings
from ai.preprocessing.normalization import DataFrameNormalizer
from ai.preprocessing.windowing import create_windows
from ai.features.feature_engineering import (
    extract_window_features,
    extract_features_from_windows,
)
from ai.features.rolling_features import calculate_rolling_features


# ==========================================
# CLEANING TESTS
# ==========================================

def sample_data():
    return pd.DataFrame({
        "timestamp": [
            "2026-11-01T10:00:00Z",
            "2026-11-01T10:01:00Z",
            "2026-11-01T10:02:00Z",
        ],
        "heart_rate": [75, 80, 85],
        "spo2": [98, 97, 96],
        "scenario": ["normal", "normal", "heatwave"],
    })


def test_valid_data_is_preserved():
    result = clean_readings(sample_data())
    assert len(result) == 3
    assert result["heart_rate"].tolist() == [75, 80, 85]


def test_invalid_timestamp_is_removed():
    data = sample_data()
    data.loc[1, "timestamp"] = "invalid"

    result = clean_readings(data)
    assert len(result) == 2


def test_invalid_numeric_value_becomes_nan():
    data = sample_data()
    data["heart_rate"] = data["heart_rate"].astype(object)
    data.loc[0, "heart_rate"] = "invalid"

    result = clean_readings(data)
    assert pd.isna(result.loc[0, "heart_rate"])


def test_duplicate_records_are_removed():
    data = pd.concat(
        [sample_data(), sample_data().iloc[[0]]],
        ignore_index=True,
    )

    result = clean_readings(data)
    assert len(result) == 3


def test_missing_timestamp_column_raises_error():
    data = sample_data().drop(columns=["timestamp"])

    with pytest.raises(ValueError):
        clean_readings(data)


def test_empty_dataframe_raises_error():
    with pytest.raises(ValueError):
        clean_readings(pd.DataFrame())


def test_partially_missing_sensor_data_is_preserved():
    data = sample_data()
    data.loc[0, "heart_rate"] = None

    result = clean_readings(data)
    assert len(result) == 3
    assert pd.isna(result.loc[0, "heart_rate"])


def test_timestamp_is_converted_to_utc():
    result = clean_readings(sample_data())

    assert str(result["timestamp"].dtype) == "datetime64[ns, UTC]"


# ==========================================
# NORMALIZATION TESTS
# ==========================================

def test_standard_scaling():
    data = pd.DataFrame({
        "heart_rate": [70, 80, 90],
        "spo2": [96, 97, 98],
    })

    normalizer = DataFrameNormalizer(method="standard")
    result = normalizer.fit_transform(data)

    assert abs(result["heart_rate"].mean()) < 1e-9
    assert abs(result["spo2"].mean()) < 1e-9


def test_minmax_scaling():
    data = pd.DataFrame({
        "heart_rate": [70, 80, 90],
        "spo2": [96, 97, 98],
    })

    normalizer = DataFrameNormalizer(method="minmax")
    result = normalizer.fit_transform(data)

    assert result["heart_rate"].min() == 0
    assert result["heart_rate"].max() == 1


def test_non_numeric_columns_are_preserved():
    data = pd.DataFrame({
        "heart_rate": [70, 80, 90],
        "scenario": ["normal", "normal", "heatwave"],
    })

    normalizer = DataFrameNormalizer()
    result = normalizer.fit_transform(data)

    assert result["scenario"].tolist() == data["scenario"].tolist()


def test_transform_uses_training_parameters():
    train = pd.DataFrame({"heart_rate": [70, 80, 90]})
    test = pd.DataFrame({"heart_rate": [100]})

    normalizer = DataFrameNormalizer(method="standard")
    normalizer.fit(train)

    result = normalizer.transform(test)

    assert result.loc[0, "heart_rate"] > 1


def test_transform_before_fit_raises_error():
    normalizer = DataFrameNormalizer()
    data = pd.DataFrame({"heart_rate": [70, 80, 90]})

    with pytest.raises(RuntimeError):
        normalizer.transform(data)


def test_invalid_method_raises_error():
    with pytest.raises(ValueError):
        DataFrameNormalizer(method="invalid")


def test_missing_numerical_column_raises_error():
    train = pd.DataFrame({
        "heart_rate": [70, 80, 90],
        "spo2": [96, 97, 98],
    })

    test = pd.DataFrame({"heart_rate": [75]})

    normalizer = DataFrameNormalizer()
    normalizer.fit(train)

    with pytest.raises(ValueError):
        normalizer.transform(test)


def test_missing_values_are_preserved():
    data = pd.DataFrame({
        "heart_rate": [70, None, 90],
        "spo2": [96, 97, 98],
    })

    normalizer = DataFrameNormalizer()
    result = normalizer.fit_transform(data)

    assert pd.isna(result.loc[1, "heart_rate"])


# ==========================================
# WINDOWING TESTS
# ==========================================

def window_sample_data():
    return pd.DataFrame({
        "timestamp": pd.date_range(
            "2026-11-01 10:00:00",
            periods=5,
            freq="2s",
            tz="UTC",
        ),
        "heart_rate": [75, 77, 79, 83, 88],
        "spo2": [99, 98, 98, 97, 96],
    })


def test_correct_number_of_windows():
    result = create_windows(
        window_sample_data(),
        window_size=3,
        stride=1,
    )

    assert len(result) == 3


def test_window_contents_are_correct():
    result = create_windows(
        window_sample_data(),
        window_size=3,
        stride=1,
    )

    assert result[0]["heart_rate"].tolist() == [75, 77, 79]
    assert result[1]["heart_rate"].tolist() == [77, 79, 83]
    assert result[2]["heart_rate"].tolist() == [79, 83, 88]


def test_non_overlapping_windows():
    result = create_windows(
        window_sample_data(),
        window_size=2,
        stride=2,
    )

    assert len(result) == 2
    assert result[0]["heart_rate"].tolist() == [75, 77]
    assert result[1]["heart_rate"].tolist() == [79, 83]


def test_readings_are_sorted_chronologically():
    data = window_sample_data().iloc[::-1]

    result = create_windows(
        data,
        window_size=5,
        stride=1,
    )

    assert result[0]["heart_rate"].tolist() == [75, 77, 79, 83, 88]


def test_insufficient_readings_return_no_windows():
    data = window_sample_data().iloc[:2]

    result = create_windows(
        data,
        window_size=3,
    )

    assert result == []


def test_invalid_window_size_raises_error():
    with pytest.raises(ValueError):
        create_windows(window_sample_data(), window_size=0)


def test_invalid_stride_raises_error():
    with pytest.raises(ValueError):
        create_windows(
            window_sample_data(),
            window_size=3,
            stride=0,
        )


def test_missing_timestamp_column_raises_error():
    data = window_sample_data().drop(columns=["timestamp"])

    with pytest.raises(ValueError):
        create_windows(data, window_size=3)


# ==========================================
# FEATURE ENGINEERING TESTS
# ==========================================

def test_mean_feature():
    data = pd.DataFrame({"heart_rate": [70, 80, 90]})

    result = extract_window_features(data)

    assert result["heart_rate_mean"] == 80


def test_minimum_and_maximum_features():
    data = pd.DataFrame({"heart_rate": [70, 80, 90]})

    result = extract_window_features(data)

    assert result["heart_rate_min"] == 70
    assert result["heart_rate_max"] == 90


def test_range_feature():
    data = pd.DataFrame({"heart_rate": [70, 80, 90]})

    result = extract_window_features(data)

    assert result["heart_rate_range"] == 20


def test_increasing_trend_is_positive():
    data = pd.DataFrame({"heart_rate": [70, 75, 80, 85]})

    result = extract_window_features(data)

    assert result["heart_rate_trend"] > 0


def test_decreasing_trend_is_negative():
    data = pd.DataFrame({"spo2": [99, 98, 97, 96]})

    result = extract_window_features(data)

    assert result["spo2_trend"] < 0


def test_missing_values_are_ignored():
    data = pd.DataFrame({
        "heart_rate": [70, None, 90],
    })

    result = extract_window_features(data)

    assert result["heart_rate_mean"] == 80


def test_multiple_windows_create_feature_table():
    windows = [
        pd.DataFrame({"heart_rate": [70, 80, 90]}),
        pd.DataFrame({"heart_rate": [80, 90, 100]}),
    ]

    result = extract_features_from_windows(windows)

    assert len(result) == 2
    assert "heart_rate_mean" in result.columns


def test_empty_window_raises_error():
    with pytest.raises(ValueError):
        extract_window_features(pd.DataFrame())


def test_single_value_has_nan_std_and_trend():
    data = pd.DataFrame({"heart_rate": [75]})

    result = extract_window_features(data)

    assert result["heart_rate_mean"] == 75
    assert pd.isna(result["heart_rate_std"])
    assert pd.isna(result["heart_rate_trend"])


# ==========================================
# ROLLING FEATURES TESTS
# ==========================================


def test_rolling_mean():
    data = pd.DataFrame({"heart_rate": [75, 77, 79, 83]})

    result = calculate_rolling_features(data, window_size=3)

    assert pd.isna(result.loc[0, "heart_rate_rolling_mean"])
    assert result.loc[2, "heart_rate_rolling_mean"] == 77


def test_rolling_standard_deviation():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    result = calculate_rolling_features(data, window_size=3)

    assert round(result.loc[2, "heart_rate_rolling_std"], 2) == 2.00


def test_rolling_minimum_and_maximum():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    result = calculate_rolling_features(data, window_size=3)

    assert result.loc[2, "heart_rate_rolling_min"] == 75
    assert result.loc[2, "heart_rate_rolling_max"] == 79


def test_rolling_range():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    result = calculate_rolling_features(data, window_size=3)

    assert result.loc[2, "heart_rate_rolling_range"] == 4


def test_original_columns_are_preserved():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    result = calculate_rolling_features(data, window_size=2)

    assert "heart_rate" in result.columns
    assert result["heart_rate"].tolist() == [75, 77, 79]


def test_multiple_features_are_calculated():
    data = pd.DataFrame({
        "heart_rate": [75, 77, 79],
        "spo2": [99, 98, 97],
    })

    result = calculate_rolling_features(data, window_size=2)

    assert "heart_rate_rolling_mean" in result.columns
    assert "spo2_rolling_mean" in result.columns


def test_custom_min_periods():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    result = calculate_rolling_features(
        data,
        window_size=3,
        min_periods=1,
    )

    assert result.loc[0, "heart_rate_rolling_mean"] == 75


def test_invalid_window_size_raises_error():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    with pytest.raises(ValueError):
        calculate_rolling_features(data, window_size=0)


def test_invalid_min_periods_raises_error():
    data = pd.DataFrame({"heart_rate": [75, 77, 79]})

    with pytest.raises(ValueError):
        calculate_rolling_features(
            data,
            window_size=3,
            min_periods=4,
        )

