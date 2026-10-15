import time
from typing import Iterator, Optional

from simulator.config import DEFAULT_SCENARIO, SIMULATION_INTERVAL
from simulator.data_generator import generate_data
from simulator.client import post_reading


def stream_data(scenario: str, count: Optional[int] = None) -> Iterator[dict]:
    """Yield simulated records for a finite run or indefinitely."""
    generated = 0
    while count is None or generated < count:
        yield generate_data(scenario)
        generated += 1


def run_simulator(
    scenario: str,
    count: Optional[int] = None,
    endpoint: Optional[str] = None,
) -> None:
    """Print simulated data for a finite run or continuously."""
    print("----------------------------------------")
    print("Personal Health Companion")
    print("Health Data Simulator")
    print("----------------------------------------")
    print(f"Scenario : {scenario}")
    print(f"Interval : {SIMULATION_INTERVAL} seconds")
    print("Press CTRL+C to stop.")
    print("----------------------------------------")

    try:
        for data in stream_data(scenario, count):
            print(data)
            if endpoint:
                print(post_reading(data, endpoint=endpoint))
            if count is None:
                time.sleep(SIMULATION_INTERVAL)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    run_simulator(DEFAULT_SCENARIO)
