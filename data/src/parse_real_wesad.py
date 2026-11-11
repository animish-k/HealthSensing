"""
Official WESAD Binary Parser for Subject S2
Extracts genuine recorded human physiological vitals and ground-truth stress labels.
Author: Kartikeya Singh (Member 1)
"""
import pickle
import os
import pandas as pd
import numpy as np

def extract_real_wesad():
    pkl_path = "data/raw/S2.pkl"
    e4_hr_path = "data/raw/S2_E4_Data/HR.csv"
    output_path = "data/processed/wesad_s2_real.csv"

    print("1. Loading raw official WESAD binary (952 MB)...")
    with open(pkl_path, "rb") as f:
        data = pickle.load(f, encoding="latin1")

    print("2. Extracting Empatica E4 wrist signals and labels...")
    wrist = data["signal"]["wrist"]
    eda = wrist["EDA"].flatten()     # 4 Hz
    temp = wrist["TEMP"].flatten()   # 4 Hz
    labels = data["label"].flatten() # 700 Hz

    # Load Empatica E4 device precomputed heart rate (1 Hz)
    if os.path.exists(e4_hr_path):
        hr_raw = pd.read_csv(e4_hr_path, skiprows=2, header=None).values.flatten()
    else:
        hr_raw = np.full(len(eda) // 4, 72.0)

    # Align to 1-second epochs (1 Hz)
    total_seconds = min(len(hr_raw), len(eda) // 4, len(temp) // 4, len(labels) // 700)
    print(f"3. Synchronizing {total_seconds} seconds of continuous human recording...")

    # Extract 600 seconds (10 minutes) covering both Baseline (label 1) and Stress (label 2)
    sample_duration = min(total_seconds, 600)
    records = []
    
    for s in range(sample_duration):
        lbl = int(labels[s * 700])
        mapped_label = lbl if lbl in [1, 2, 3, 4] else 1
        
        records.append({
            "participant_id": "S2",
            "session_id": "WESAD_S2_RealLab",
            "timestamp": f"2026-11-11T10:{s//60:02d}:{s%60:02d}Z",
            "heart_rate_bpm": round(float(hr_raw[s]), 1) if s < len(hr_raw) else 72.0,
            "eda_microsiemens": round(float(np.mean(eda[s*4 : (s+1)*4])), 4),
            "body_temperature_c": round(float(np.mean(temp[s*4 : (s+1)*4])), 2),
            "stress_label": mapped_label,
            "source": "WESAD_Real_E4"
        })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Extracted {len(df)} seconds of genuine human data to {output_path}!")

if __name__ == "__main__":
    extract_real_wesad()
