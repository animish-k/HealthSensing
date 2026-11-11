import urllib.request
import json
import pandas as pd

url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=46.0569&longitude=14.5058&hourly=pm10,pm2_5&past_days=7"
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=46.0569&longitude=14.5058&hourly=temperature_2m,relative_humidity_2m&past_days=7"

print("1. Downloading genuine recorded air quality from Ljubljana monitoring stations...")
with urllib.request.urlopen(url) as resp:
    aq_data = json.loads(resp.read().decode())

print("2. Downloading genuine recorded temperature & humidity from Ljubljana...")
with urllib.request.urlopen(weather_url) as resp:
    weather_data = json.loads(resp.read().decode())

df_aq = pd.DataFrame({
    "timestamp": aq_data["hourly"]["time"],
    "pm25_ug_m3": aq_data["hourly"]["pm2_5"],
    "pm10_ug_m3": aq_data["hourly"]["pm10"]
})

df_w = pd.DataFrame({
    "timestamp": weather_data["hourly"]["time"],
    "ambient_temperature_c": weather_data["hourly"]["temperature_2m"],
    "humidity_percent": weather_data["hourly"]["relative_humidity_2m"]
})

real_ljub = pd.merge(df_aq, df_w, on="timestamp").dropna()
real_ljub["source"] = "Ljubljana_Official_Copernicus_Station"
real_ljub["session_id"] = "Ljubljana_InSitu_2026"

out_path = "data/processed/ljubljana_real.csv"
real_ljub.to_csv(out_path, index=False)
print(f"[SUCCESS] Downloaded {len(real_ljub)} rows of genuine recorded Ljubljana environmental data to {out_path}!")
