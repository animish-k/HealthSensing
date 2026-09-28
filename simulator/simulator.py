import random
import time
from datetime import datetime

from config import SIMULATION_INTERVAL, DEFAULT_SCENARIO
from scenarios import SCENARIOS


def random_value(value_range):
    """
    Generate a random value within the given range.

    Example:
        (65, 85) → random value between 65 and 85
    """

    return random.uniform(value_range[0], value_range[1])


def generate_data(scenario):
    """
    Generate one health/environment data record
    based on the selected scenario.
    """

    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    ranges = SCENARIOS[scenario]

    data = {
        "timestamp": datetime.now().isoformat(),

        "scenario": scenario,

        "heart_rate": round(
            random_value(ranges["heart_rate"])
        ),

        "spo2": round(
            random_value(ranges["spo2"]),
            1
        ),

        "body_temperature": round(
            random_value(ranges["body_temperature"]),
            1
        ),

        "activity_level": round(
            random_value(ranges["activity_level"]),
            2
        ),

        "ambient_temperature": round(
            random_value(ranges["ambient_temperature"]),
            1
        ),

        "humidity": round(
            random_value(ranges["humidity"]),
            1
        ),

        "aqi": round(
            random_value(ranges["aqi"])
        ),

        "pm25": round(
            random_value(ranges["pm25"]),
            1
        )
    }

    return data


def run_simulator(scenario):
    """
    Continuously generate simulated data.
    """

    print("----------------------------------------")
    print("Personal Health Companion")
    print("Health Data Simulator")
    print("----------------------------------------")
    print(f"Scenario : {scenario}")
    print(f"Interval : {SIMULATION_INTERVAL} seconds")
    print("Press CTRL+C to stop.")
    print("----------------------------------------")

    try:

        while True:

            data = generate_data(scenario)

            print(data)

            time.sleep(SIMULATION_INTERVAL)

    except KeyboardInterrupt:

        print("\nSimulator stopped.")


if __name__ == "__main__":

    run_simulator(DEFAULT_SCENARIO)