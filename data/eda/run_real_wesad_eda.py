import pandas as pd
import matplotlib.pyplot as plt
from data.src.cleaner import clean_dataframe
from data.src.features import extract_window_features, summarize_personal_baseline

df_real = pd.read_csv("data/processed/wesad_s2_real.csv")
cleaned = clean_dataframe(df_real)

# Calibrate personal baseline on Subject 2's resting baseline condition (label 1)
baseline_data = cleaned[cleaned["stress_label"] == 1]
baseline = summarize_personal_baseline(baseline_data)
features = extract_window_features(cleaned, window_size=5, baseline_stats=baseline)

# Plot 1: Real Vitals Dynamics with Baseline Band
plt.figure(figsize=(10, 5))
plt.plot(features.index, features["heart_rate_bpm"], label="Actual Subject S2 HR (Empatica E4)", color="#2980b9", alpha=0.6)
plt.plot(features.index, features["heart_rate_bpm_rolling_mean"], label="5-sec Rolling Mean", color="#c0392b", linewidth=2)
if "heart_rate_bpm" in baseline:
    b_mean = baseline["heart_rate_bpm"]["mean"]
    b_std = baseline["heart_rate_bpm"]["std"]
    plt.axhline(b_mean, color="green", linestyle="--", label=f"Personal Baseline Mean ({b_mean} bpm)")
    plt.axhspan(b_mean - b_std, b_mean + b_std, color="green", alpha=0.15, label="Normal Band (±1 Std)")

plt.title("WESAD Subject S2: Genuine Human Heart Rate Dynamics & Baseline", fontsize=11)
plt.xlabel("Recording Timeline (Seconds)")
plt.ylabel("Heart Rate (bpm)")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("data/eda/plots/real_wesad_s2_vital_dynamics.png", dpi=200)
plt.close()

# Plot 2: Real Electrodermal Activity (Sweat Response)
plt.figure(figsize=(10, 4.5))
plt.plot(features.index, features["eda_microsiemens"], color="#8e44ad", linewidth=1.5, label="Sympathetic EDA (microSiemens)")
plt.title("WESAD Subject S2: Genuine Electrodermal Activity (EDA / GSR)", fontsize=11)
plt.xlabel("Recording Timeline (Seconds)")
plt.ylabel("EDA (microSiemens)")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("data/eda/plots/real_wesad_s2_eda_dynamics.png", dpi=200)
plt.close()

print("Generated real EDA plots successfully from genuine Subject S2 recordings!")
