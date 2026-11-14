import os
import pickle
from datetime import datetime, timezone
import numpy as np
import pandas as pd

SUBJECTS = ["S2", "S3", "S4", "S5"]

def read_e4_header_and_values(csv_path: str):
    with open(csv_path, "r") as f:
        start_ts = float(f.readline().strip().split(",")[0])
        sample_rate = float(f.readline().strip().split(",")[0])
    values = pd.read_csv(csv_path, skiprows=2, header=None).values.flatten()
    return start_ts, sample_rate, values

def parse_subject(sub_id: str):
    pkl_path = f"data/raw/{sub_id}.pkl"
    e4_dir = f"data/raw/{sub_id}_E4_Data"
    hr_path = os.path.join(e4_dir, "HR.csv")
    eda_path = os.path.join(e4_dir, "EDA.csv")
    output_path = f"data/processed/wesad_{sub_id.lower()}_real.csv"

    if not os.path.exists(pkl_path):
        print(f"[SKIP] {pkl_path} not found.")
        return None

    print(f"\n{'='*65}")
    print(f"Processing {sub_id} ({pkl_path})...")
    with open(pkl_path, "rb") as f:
        data = pickle.load(f, encoding="latin1")

    wrist = data["signal"]["wrist"]
    eda = wrist["EDA"].flatten()
    temp = wrist["TEMP"].flatten()
    labels = data["label"].flatten()

    total_seconds = min(len(eda) // 4, len(temp) // 4, len(labels) // 700)

    if os.path.exists(hr_path) and os.path.exists(eda_path):
        hr_start_ts, _, hr_raw = read_e4_header_and_values(hr_path)
        eda_start_ts, _, _ = read_e4_header_and_values(eda_path)
        hr_offset_sec = int(round(hr_start_ts - eda_start_ts))
        session_start_ts = eda_start_ts
    elif os.path.exists(hr_path):
        hr_start_ts, _, hr_raw = read_e4_header_and_values(hr_path)
        hr_offset_sec = 0
        session_start_ts = hr_start_ts
    else:
        hr_raw = np.array([])
        hr_offset_sec = 0
        session_start_ts = None

    print(f"  Stream lengths -> EDA(4Hz): {len(eda)}, TEMP(4Hz): {len(temp)}, Label(700Hz): {len(labels)}")
    print(f"  Aligned 1Hz duration: {total_seconds} s | HR.csv offset vs session start: {hr_offset_sec:+d} s | HR samples: {len(hr_raw)}")

    records = []
    for s in range(total_seconds):
        midpoint_idx = s * 700 + 350
        raw_label = int(labels[midpoint_idx])

        hr_idx = s - hr_offset_sec
        if len(hr_raw) > 0 and 0 <= hr_idx < len(hr_raw) and not np.isnan(hr_raw[hr_idx]):
            hr_val = round(float(hr_raw[hr_idx]), 2)
        else:
            hr_val = np.nan

        if session_start_ts is not None:
            ts_str = datetime.fromtimestamp(session_start_ts + s, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            ts_str = f"2026-11-11T{(s//3600):02d}:{(s%3600)//60:02d}:{s%60:02d}Z"

        records.append({
            "participant_id": sub_id,
            "session_id": f"WESAD_{sub_id}_RealLab",
            "timestamp": ts_str,
            "heart_rate_bpm": hr_val,
            "eda_microsiemens": round(float(np.mean(eda[s * 4 : (s + 1) * 4])), 4),
            "body_temperature_c": round(float(np.mean(temp[s * 4 : (s + 1) * 4])), 2),
            "stress_label": raw_label,
            "source": "WESAD_Real_E4"
        })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)

    missing_hr = int(df["heart_rate_bpm"].isna().sum())
    label_counts = df["stress_label"].value_counts().sort_index().to_dict()
    print(f"  Saved: {output_path} ({len(df)} rows, missing HR: {missing_hr})")
    print(f"  Label distribution (0=transient, 1=baseline, 2=stress, 3=amusement, 4=meditation): {label_counts}")
    return {"participant_id": sub_id, "rows": len(df), "missing_hr": missing_hr, "hr_offset_sec": hr_offset_sec, **label_counts}

if __name__ == "__main__":
    summary = []
    for sub in SUBJECTS:
        res = parse_subject(sub)
        if res:
            summary.append(res)
    print("\n" + "="*65)
    print("SUMMARY ACROSS ALL PARTICIPANTS:")
    print(pd.DataFrame(summary).fillna(0).to_string(index=False))
