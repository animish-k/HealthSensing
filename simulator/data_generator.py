from datetime import datetime, timezone
import random
from typing import Optional

from simulator.scenarios import SCENARIOS


def random_value(value_range, rng) -> float:
    return rng.uniform(value_range[0], value_range[1])


def generate_data(
    scenario: str,
    rng: Optional[random.Random] = None,
) -> dict:
    """Generate one schema-compatible simulated reading."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    generator = rng or random
    ranges = SCENARIOS[scenario]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "simulator",
        "scenario": scenario,
        "heart_rate": round(random_value(ranges["heart_rate"], generator)),
        "spo2": round(random_value(ranges["spo2"], generator), 1),
        "body_temperature": round(
            random_value(ranges["body_temperature"], generator), 1
        ),
        "activity_level": round(
            random_value(ranges["activity_level"], generator), 2
        ),
        "ambient_temperature": round(
            random_value(ranges["ambient_temperature"], generator), 1
        ),
        "humidity": round(random_value(ranges["humidity"], generator), 1),
        "aqi": round(random_value(ranges["aqi"], generator)),
        "pm25": round(random_value(ranges["pm25"], generator), 1),
    }