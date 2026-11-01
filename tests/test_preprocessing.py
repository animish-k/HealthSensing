
import pandas as pd
import pytest

from ai.preprocessing.cleaning import clean_readings


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
