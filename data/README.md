# HealthSensing Data Pipeline & Inventory

**Owner:** Kartikeya Singh (Member 1)  
**Deliverables:** Data Acquisition, Exploratory Data Analysis (EDA), and Preprocessing

## 1. Candidate Dataset Inventory
- **WESAD:** Multimodal wearable dataset (ECG, BVP, EDA, TEMP). Used for physiological baseline and stress benchmarking.
- **Ljubljana Environmental/Biometric:** Combined PM2.5, ambient temp, humidity, and wearable heart rate. Used for environmental context evaluation.
- **Google Pixel Watch:** Personal wearable exports used for individual baseline reference and routine modeling.

## 2. Pipeline Modules
- `data/src/cleaner.py`: Rejects physiological sensor outliers and aligns chronological timestamps.
- `data/src/features.py`: Computes rolling window statistics, slopes/deltas, and personal baseline deviations.
- `data/samples/sample_processed.json`: Test fixtures matching the shared team schema.
