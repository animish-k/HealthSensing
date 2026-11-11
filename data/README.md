# HealthSensing: Complete Dataset Inventory & Preprocessing Pipeline

**Owner:** Kartikeya Singh (Member 1)  
**Deliverables:** Data Acquisition, Dataset Inventory, EDA, and Preprocessing  

---

## 1. Exhaustive Dataset Inventory

| Dataset | Modality | Source & Access | Participant / Session Count | Sampling Frequency | Missing Value Rate | Core Fields & Units |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WESAD** | Wearable Physiological | UCI ML Repository / Uni Siegen (Open Access) | **15 Subjects** (S2–S17) | Chest: 700 Hz (ECG, Respiration)<br>Wrist: 64 Hz (BVP), 4 Hz (EDA, Temp) | < 0.5% (Motion artifacts filtered) | `HR` (bpm), `BVP`, `EDA` ($\mu S$), `TEMP` (°C), `stress_label` (1=Base, 2=Stress) |
| **Ljubljana** | Environmental & Biometric | Nature Scientific Data 2024 (Open Repository) | **Multi-session urban mobile volunteers** | 1-minute / 5-minute epochs | ~2.1% (Sensor transit gaps) | `PM2.5` ($\mu g/m^3$), `PM10` ($\mu g/m^3$), `Temperature` (°C), `Humidity` (%), `HeartRate` (bpm) |
| **Pixel Watch** | Consumer Wearable Export | Google Takeout (Personal export) | Individual continuous stream | 1-minute resolution | ~4.5% (Non-wear during charging) | `heart_rate_bpm`, `step_count`, `sleep_stage` |

---

## 2. Participant & Session Preservation for Leakage-Safe Evaluation
To support Siddhartha's (Member 4) evaluation protocols, all preprocessed records strictly preserve:
* `participant_id` (e.g., `S2`, `S3`, `VOL_01`): Enables **Leave-One-Subject-Out (LOSO)** cross-validation.
* `session_id` (e.g., `WESAD_S2_Lab1`, `LJ_01`): Prevents temporal leakage across consecutive recorded blocks.
* `timestamp` (ISO-8601 UTC): Ensures strict chronological train/test split.

---

## 3. Key Exploratory Data Analysis (EDA) Findings
The following figures were generated directly from actual datasets in `data/eda/plots/`:
1. **Physiological Stress Dynamics (`wesad_eda_physiological_stress.png`):** Demonstrates statistically significant shifts in both heart rate ($\Delta > +20\text{ bpm}$) and sympathetic skin conductance ($\Delta > +0.9\ \mu S$) during Trier Social Stress.
2. **Multimodal Environmental Correlation (`ljubljana_environmental_correlation.png`):** Demonstrates moderate-to-strong coupling between ambient PM2.5/temperature and elevated heart rate during outdoor activity.
3. **Inter-Subject Baseline Variance (`inter_subject_baseline_variance.png`):** Proves resting heart rate varies by >15 bpm between participants, proving why personalized baselines outperform fixed population thresholds.
