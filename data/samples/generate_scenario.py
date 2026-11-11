import json
import numpy as np

np.random.seed(42)
records = []
for minute in range(60):
    ts = f"2026-11-11T10:{minute:02d}:00Z"
    if minute < 20:
        hr = round(float(np.random.normal(72, 2)), 1)
        spo2 = 98.0
        amb_temp = round(float(np.random.normal(26.0, 0.5)), 1)
        aqi = round(float(np.random.normal(40, 3)), 1)
        activity = "sedentary"
    elif minute < 40:
        progress = (minute - 20) / 20.0
        hr = round(float(np.random.normal(72 + progress * 24, 3)), 1)
        spo2 = round(float(np.random.normal(98 - progress * 2.5, 0.5)), 1)
        amb_temp = round(float(np.random.normal(26.0 + progress * 8.5, 0.8)), 1)
        aqi = round(float(np.random.normal(40 + progress * 95, 6)), 1)
        activity = "walking"
    else:
        progress = (minute - 40) / 20.0
        hr = round(float(np.random.normal(96 - progress * 20, 2)), 1)
        spo2 = round(float(np.random.normal(95.5 + progress * 2.5, 0.3)), 1)
        amb_temp = round(float(np.random.normal(34.5 - progress * 7.0, 0.5)), 1)
        aqi = round(float(np.random.normal(135 - progress * 85, 4)), 1)
        activity = "sedentary"

    records.append({
        "timestamp": ts,
        "source": "wearable",
        "heart_rate_bpm": hr,
        "spo2_percent": spo2,
        "ambient_temperature_c": amb_temp,
        "humidity_percent": 65.0,
        "aqi": aqi,
        "activity_level": activity
    })

with open("data/samples/stress_scenario_sample.json", "w") as f:
    json.dump(records, f, indent=2)

print("Generated 60-minute scenario stream in data/samples/stress_scenario_sample.json")
