import pandas as pd
import numpy as np

np.random.seed(42)

# 1. WESAD Multi-Subject Dataset (Subjects S2, S3, S4)
wesad_records = []
for sub_id, base_hr in [("S2", 71.0), ("S3", 78.5), ("S4", 65.0)]:
    for i in range(60):
        ts = f"2026-11-11T10:{i:02d}:00Z"
        if i < 30:
            hr = round(float(np.random.normal(base_hr, 2.0)), 1)
            eda = round(float(np.random.normal(0.35, 0.05)), 3)
            temp = round(float(np.random.normal(32.4, 0.2)), 2)
            lbl = 1
        else:
            hr = round(float(np.random.normal(base_hr + 22.0, 3.5)), 1)
            eda = round(float(np.random.normal(1.25, 0.15)), 3)
            temp = round(float(np.random.normal(33.5, 0.3)), 2)
            lbl = 2

        wesad_records.append({
            "participant_id": sub_id,
            "session_id": f"WESAD_{sub_id}_Lab1",
            "timestamp": ts,
            "HR": hr,
            "EDA": eda,
            "TEMP": temp,
            "BVP": round(float(np.random.normal(0, 15)), 1),
            "label": lbl
        })

pd.DataFrame(wesad_records).to_csv("data/raw_samples/wesad_multisubject.csv", index=False)
print("Created: data/raw_samples/wesad_multisubject.csv (Subjects S2, S3, S4)")

# 2. Ljubljana Multi-Session Dataset (Sessions LJ_01, LJ_02)
ljub_records = []
for sess_id, base_hr in [("LJ_01", 73.0), ("LJ_02", 82.0)]:
    for i in range(50):
        ts = f"2026-11-11T12:{i:02d}:00Z"
        pm25 = round(float(np.random.normal(15.0 + (i * 1.8), 3.0)), 1)
        pm10 = round(pm25 * 1.4, 1)
        temp = round(float(np.random.normal(25.0 + (i * 0.18), 0.5)), 1)
        hum = round(float(np.random.normal(58.0 + (i * 0.3), 1.0)), 1)
        hr = round(float(np.random.normal(base_hr + (i * 0.45), 2.0)), 1)

        ljub_records.append({
            "participant_id": f"VOL_{sess_id[-2:]}",
            "session_id": sess_id,
            "timestamp": ts,
            "PM2.5": pm25,
            "PM10": pm10,
            "Temperature": temp,
            "Humidity": hum,
            "HeartRate": hr
        })

pd.DataFrame(ljub_records).to_csv("data/raw_samples/ljubljana_multisession.csv", index=False)
print("Created: data/raw_samples/ljubljana_multisession.csv (Sessions LJ_01, LJ_02)")
