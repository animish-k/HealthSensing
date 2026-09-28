# Scenario configurations for the health-data simulator


SCENARIOS = {

    "normal": {
        "heart_rate": (65, 85),
        "spo2": (96, 99),
        "body_temperature": (36.5, 37.2),
        "activity_level": (0.2, 0.6),
        "ambient_temperature": (25, 32),
        "humidity": (40, 70),
        "aqi": (40, 100),
        "pm25": (10, 50)
    },

    "heatwave": {
        "heart_rate": (90, 120),
        "spo2": (94, 98),
        "body_temperature": (37.2, 38.5),
        "activity_level": (0.6, 1.0),
        "ambient_temperature": (36, 45),
        "humidity": (60, 90),
        "aqi": (50, 120),
        "pm25": (15, 60)
    },

    "pollution": {
        "heart_rate": (75, 105),
        "spo2": (90, 96),
        "body_temperature": (36.5, 37.4),
        "activity_level": (0.2, 0.7),
        "ambient_temperature": (25, 32),
        "humidity": (40, 75),
        "aqi": (150, 350),
        "pm25": (80, 250)
    },

    "fatigue": {
        "heart_rate": (65, 100),
        "spo2": (94, 98),
        "body_temperature": (36.5, 37.3),
        "activity_level": (0.05, 0.3),
        "ambient_temperature": (25, 32),
        "humidity": (40, 70),
        "aqi": (40, 100),
        "pm25": (10, 50)
    }
}