
"""Example of calling the HealthSensing baseline detector.

This is an integration example, not a FastAPI endpoint.
"""

from ai.baseline.personal_baseline import detect_anomalies


def analyze_heart_rate(
    readings: list[float],
    baseline_readings: list[float],
) -> list[dict]:
    """Return JSON-serializable anomaly results for backend use."""
    result = detect_anomalies(
        readings=readings,
        baseline_readings=baseline_readings,
        threshold=3.0,
    )

    # Convert the DataFrame into ordinary Python dictionaries.
    return result.to_dict(orient="records")


if __name__ == "__main__":
    baseline = [72.0, 74.0, 73.0, 75.0, 71.0, 74.0]
    incoming_readings = [73.0, 75.0, 96.0]

    output = analyze_heart_rate(incoming_readings, baseline)

    for reading in output:
        print(reading)
