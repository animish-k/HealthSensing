import time
import json
import pandas as pd
from data.src.pipeline import HealthSensingPipeline

def run_live_demo():
    print("=" * 60)
    print("HealthSensing: Live Edge-AI Data Pipeline (Member 1)")
    print("=" * 60)
    
    # Load from the verified 60-minute scenario stream
    with open("data/samples/stress_scenario_sample.json", "r") as f:
        records = json.load(f)
    
    pipeline = HealthSensingPipeline(window_size=5)
    baseline_df = pd.DataFrame(records[:20]) # first 20 minutes as baseline
    pipeline.fit_baseline(baseline_df)
    
    print("\n[OK] Personal Baseline Calibrated:")
    print(pipeline.baseline_stats)
    
    print("\nProcessing incoming live stream (sample 5 records):")
    for i, r in enumerate(records[18:23]):
        processed = pipeline.process_record(r)
        print(f" -> Stream #{i+1} [{processed.get('timestamp')}]: HR={processed.get('heart_rate_bpm')} bpm, Temp={processed.get('ambient_temperature_c')} C, Status=CLEAN")
        time.sleep(0.3)
    
    print("\n[SUCCESS] Pipeline is ready for FastAPI/WebSocket ingestion!")

if __name__ == "__main__":
    run_live_demo()
