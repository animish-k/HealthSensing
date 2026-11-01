

import pandas as pd
import pytest

from ai.preprocessing.cleaning import clean_readings
from ai.preprocessing.normalization import DataFrameNormalizer


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


# CLEANING TESTS


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


# NORMALIZATION TESTS


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
