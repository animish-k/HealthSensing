# HealthSensing Data Engineering & Preprocessing Documentation

**Owner:** Kartikeya Singh (Member 1)  
**Deliverables:** Ingestion, Multi-Frequency Synchronization, Quality Assurance, and Normalization  

## 1. Multi-Frequency Sensor Synchronization Methodology
* **Chest RespiBAN (ECG, Respiration, Temp):** 700 Hz
* **Wrist Empatica E4 (BVP):** 64 Hz
* **Wrist Empatica E4 (EDA & Skin Temp):** 4 Hz
* **Empatica E4 Precomputed Heart Rate:** 1 Hz
* **Ground-Truth Protocol Labels:** 700 Hz

### Synchronization Strategy:
1. **Target Epoch:** All streams are resampled and aligned into **1-second non-overlapping epochs (1 Hz)**.
2. **Sub-Second Downsampling:** For 4 Hz signals (EDA and Skin Temp), we compute the 4-sample window mean over each second.
3. **Heart Rate Integration:** Empatica E4 1 Hz pulse rate is synchronized directly to the second epoch.
4. **Label Alignment:** Ground-truth labels are sampled at the epoch midpoint (s * 700) to reflect the active experimental condition.

## 2. WESAD Protocol & Ground-Truth Labels
* **0 = Transient / Undefined:** Unannotated intervals between experimental blocks.
* **1 = Baseline:** 20-minute relaxed resting condition while reading neutral magazines.
* **2 = Stress:** Trier Social Stress Test (TSST) consisting of public speaking and mental arithmetic under evaluation.
* **3 = Amusement:** Watching humorous video clips.
* **4 = Meditation:** Guided relaxation period.

> **Crucial Rule on Personal Baselines:**  
> Personal baseline means, standard deviations, and normalization parameters are fitted **strictly on stress_label == 1 (Baseline)**. Observations under stress (label == 2) are strictly evaluated relative to this calibrated baseline.

## 3. Scope & Participant Coverage
* **Active Clinical Cohort:** Subjects S2, S3, S4, and S5 are parsed and validated through the genuine data pipeline.
* **Extensibility:** The parser in data/src/parse_real_wesad.py supports unpickling any participant (S2 through S17).

## 4. End-to-End Preprocessing Sequence Execution
The complete sequence is demonstrated in `run_complete_genuine_pipeline.py`:
Real Dataset -> Loading -> Cleaning -> Feature Extraction -> Normalization -> Processed Output

Run verification:
```bash
python tests/test_preprocessing_pipeline.py
python run_complete_genuine_pipeline.py
