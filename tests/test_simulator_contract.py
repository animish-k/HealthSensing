from datetime import datetime

import pytest

from simulator.data_generator import generate_data
from simulator.simulator import stream_data


def test_generated_record_matches_backend_contract():
    record = generate_data("normal")

    assert record["source"] == "simulator"
    assert datetime.fromisoformat(record["timestamp"]).tzinfo is not None
    assert 0 <= record["activity_level"] <= 1


def test_stream_supports_finite_runs_and_rejects_unknown_scenarios():
    assert len(list(stream_data("fatigue", count=3))) == 3

    with pytest.raises(ValueError, match="Unknown scenario"):
        generate_data("unknown")
