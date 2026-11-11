import json
import pandas as pd
import matplotlib.pyplot as plt
from data.src.cleaner import clean_dataframe
from data.src.features import extract_window_features, summarize_personal_baseline

with open("data/samples/stress_scenario_sample.json", "r") as f:
    df = clean_dataframe(pd.DataFrame(json.load(f)))

baseline = summarize_personal_baseline(df.iloc[:20])
df_feats = extract_window_features(df, window_size=5, baseline_stats=baseline)

# Plot 1: Heart Rate Dynamics with Personal Baseline Band
plt.figure(figsize=(10, 5))
plt.plot(df_feats.index, df_feats["heart_rate_bpm"], label="Observed HR (bpm)", color="#3498db", alpha=0.6)
plt.plot(df_feats.index, df_feats["heart_rate_bpm_rolling_mean"], label="5-min Rolling Mean", color="#e74c3c", linewidth=2)
plt.axhline(baseline["heart_rate_bpm"]["mean"], color="green", linestyle="--", label="Personal Baseline Mean")
plt.axhspan(baseline["heart_rate_bpm"]["mean"] - baseline["heart_rate_bpm"]["std"], 
            baseline["heart_rate_bpm"]["mean"] + baseline["heart_rate_bpm"]["std"], 
            color="green", alpha=0.15, label="Normal Band (±1 Std)")
plt.title("Personalized Vital Dynamics: Baseline vs. Environmental Stress Onset", fontsize=12)
plt.xlabel("Timeline (Minutes)", fontsize=10)
plt.ylabel("Heart Rate (bpm)", fontsize=10)
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("data/eda/plots/vital_dynamics_baseline.png", dpi=200)
plt.close()

# Plot 2: Multimodal Stressor Coupling
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.plot(df_feats.index, df_feats["ambient_temperature_c"], color="#e67e22", label="Ambient Temp (°C)")
ax1.plot(df_feats.index, df_feats["aqi"], color="#9b59b6", linestyle=":", label="Air Quality Index (AQI)")
ax2.plot(df_feats.index, df_feats["heart_rate_bpm_dev_from_baseline"], color="#c0392b", linewidth=2, label="HR Baseline Deviation")
ax1.set_xlabel("Timeline (Minutes)")
ax1.set_ylabel("Environmental Stressors (Temp °C / AQI)", color="#e67e22")
ax2.set_ylabel("Physiological Deviation (bpm above baseline)", color="#c0392b")
plt.title("Multimodal Coupling: Environmental Stressors Driving Physiological Deviation", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("data/eda/plots/multimodal_stress_coupling.png", dpi=200)
plt.close()

print("Generated 2 EDA plots successfully in data/eda/plots/!")
