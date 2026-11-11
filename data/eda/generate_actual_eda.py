import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data.src.loaders import load_wesad_data, load_ljubljana_data

wesad_df = load_wesad_data("data/raw_samples/wesad_multisubject.csv")
ljub_df = load_ljubljana_data("data/raw_samples/ljubljana_multisession.csv")

# 1. WESAD Physiological Response under Stress
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
wesad_baseline = wesad_df[wesad_df["stress_label"] == 1]
wesad_stress = wesad_df[wesad_df["stress_label"] == 2]

ax1.boxplot([wesad_baseline["heart_rate_bpm"], wesad_stress["heart_rate_bpm"]])
ax1.set_xticks([1, 2], ["Baseline (Calm)", "TSST Stress"])
ax1.set_title("WESAD: Heart Rate Shift Under Stress", fontsize=11)
ax1.set_ylabel("Heart Rate (bpm)")
ax1.grid(True, alpha=0.3)

ax2.boxplot([wesad_baseline["eda_microsiemens"], wesad_stress["eda_microsiemens"]])
ax2.set_xticks([1, 2], ["Baseline (Calm)", "TSST Stress"])
ax2.set_title("WESAD: Electrodermal Activity (Sweat Response)", fontsize=11)
ax2.set_ylabel("EDA (microSiemens)")
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("data/eda/plots/wesad_eda_physiological_stress.png", dpi=200)
plt.close()

# 2. Ljubljana Correlation Heatmap
cols = ["pm25_ug_m3", "PM10", "ambient_temperature_c", "humidity_percent", "heart_rate_bpm"]
corr = ljub_df[cols].corr()

plt.figure(figsize=(7, 5.5))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Pearson Correlation")
plt.xticks(range(len(cols)), cols, rotation=35, ha="right")
plt.yticks(range(len(cols)), cols)
for i in range(len(cols)):
    for j in range(len(cols)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="black" if abs(corr.iloc[i, j]) < 0.6 else "white")
plt.title("Ljubljana: Correlation Matrix (PM2.5 vs HR)", fontsize=11)
plt.tight_layout()
plt.savefig("data/eda/plots/ljubljana_environmental_correlation.png", dpi=200)
plt.close()

# 3. Inter-Subject Baseline Variance
participants = list(wesad_df["participant_id"].unique())
baseline_hrs = [wesad_df[(wesad_df["participant_id"] == p) & (wesad_df["stress_label"] == 1)]["heart_rate_bpm"] for p in participants]

plt.figure(figsize=(8, 4.5))
plt.boxplot(baseline_hrs)
plt.xticks(range(1, len(participants) + 1), participants)
plt.axhline(100.0, color="red", linestyle="--", label="Fixed Medical Threshold (100 bpm)")
plt.title("Inter-Subject Variance: Why Fixed Thresholds Fail", fontsize=11)
plt.xlabel("Participant ID")
plt.ylabel("Resting Heart Rate (bpm)")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("data/eda/plots/inter_subject_baseline_variance.png", dpi=200)
plt.close()

print("Successfully generated 3 actual dataset EDA plots in data/eda/plots/!")
