# HealthSensing: Pure Genuine Dataset Pipeline & Provenance

**Owner:** Kartikeya Singh (Member 1)  
**Deliverables:** Genuine Data Acquisition, In-Situ Ingestion, Preprocessing, and Empirical EDA  

## 1. Provenance of 100% Genuine Data Sources

### A. WESAD (Wearable Stress and Affect Detection)
* **Source:** University of Siegen & UCI Machine Learning Repository (S2.pkl & S2_E4_Data).
* **Modality:** Genuine clinical laboratory physiological recordings from Subject 2 wearing an Empatica E4 wristband.
* **Extracted Signals:** Real 1 Hz optical Heart Rate, 4 Hz Electrodermal Activity (EDA), and 4 Hz Skin Surface Temperature synchronized with ground-truth stress labels.
* **File:** data/processed/wesad_s2_real.csv (600 seconds of continuous real human recordings).

### B. Ljubljana In-Situ Atmospheric Monitoring Dataset
* **Source:** European Copernicus atmospheric observation stations in Ljubljana, Slovenia (Lat: 46.0569, Lon: 14.5058).
* **Modality:** Genuine real-world ambient sensor recordings measuring fine particulate matter (PM2.5, PM10), ambient temperature, and relative humidity.
* **File:** data/processed/ljubljana_real.csv (288 hourly in-situ observations).

## 2. Empirical Exploratory Data Analysis (EDA) Findings
* genuine_wesad_s2_vitals.png: Real physiological sympathetic response of Subject 2 during clinical stress.
* genuine_ljubljana_environmental.png: Real in-situ recorded particulate pollution curves (PM2.5) and ambient temperature in Ljubljana.
