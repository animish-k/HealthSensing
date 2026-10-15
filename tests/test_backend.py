from datetime import datetime, timezone

import pytest

from backend.db.database import MeasurementRepository
from backend.models.measurement import Measurement


def make_measurement(**overrides):
    values = {
        "timestamp": datetime(2026, 11, 1, 15, 0, tzinfo=timezone.utc),
        "source": "simulator",
        "scenario": "normal",
        "heart_rate": 72,
        "spo2": 98,
        "body_temperature": 36.8,
        "activity_level": 0.4,
        "ambient_temperature": 28,
        "humidity": 55,
        "aqi": 50,
        "pm25": 12,
    }
    values.update(overrides)
    return Measurement(**values)


def test_measurement_requires_timezone_and_valid_ranges():
    with pytest.raises(ValueError, match="timezone"):
        make_measurement(timestamp=datetime(2026, 11, 1, 15, 0))

    with pytest.raises(ValueError):
        make_measurement(spo2=101)


def test_repository_persists_optional_fields_and_orders_recent_first(tmp_path):
    repository = MeasurementRepository(tmp_path / "health.sqlite3")
    repository.initialize()
    repository.add(
        make_measurement(
            timestamp=datetime(2026, 11, 1, 14, 0, tzinfo=timezone.utc)
        )
    )
    latest = repository.add(
        make_measurement(
            timestamp=datetime(2026, 11, 1, 15, 0, tzinfo=timezone.utc),
            spo2=None,
        )
    )

    readings = repository.recent()

    assert readings[0].id == latest.id
    assert readings[0].spo2 is None
    assert readings[1].source == "simulator"
