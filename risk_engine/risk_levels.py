from math import isfinite
from typing import Optional


AQI_CATEGORIES = (
	(0, 50, "good", "low", 0),
	(51, 100, "moderate", "moderate", 1),
	(101, 150, "unhealthy_for_sensitive_groups", "high", 2),
	(151, 200, "unhealthy", "very_high", 3),
	(201, 300, "very_unhealthy", "severe", 4),
	(301, 1000, "hazardous", "severe", 4),
)

HEAT_INDEX_CATEGORIES = (
	(80, 90, "caution", "moderate", 1),
	(90, 103, "extreme_caution", "high", 2),
	(103, 125, "danger", "very_high", 3),
	(125, float("inf"), "extreme_danger", "severe", 4),
)


def classify_aqi(value: Optional[float]) -> Optional[dict]:
	if value is None:
		return None
	if not isfinite(value) or not 0 <= value <= 1000:
		raise ValueError("AQI must be a finite value between 0 and 1000")

	rounded_value = round(value)
	for lower, upper, category, risk_level, severity in AQI_CATEGORIES:
		if lower <= rounded_value <= upper:
			return {
				"value": value,
				"category": category,
				"risk_level": risk_level,
				"severity": severity,
			}
	raise ValueError("AQI is outside the supported range")


def calculate_heat_index_celsius(
	ambient_temperature_c: float,
	relative_humidity: float,
) -> float:
	if not isfinite(ambient_temperature_c) or not -80 <= ambient_temperature_c <= 80:
		raise ValueError("ambient temperature must be finite and between -80 and 80 C")
	if not isfinite(relative_humidity) or not 0 <= relative_humidity <= 100:
		raise ValueError("relative humidity must be finite and between 0 and 100")

	temperature_f = ambient_temperature_c * 9 / 5 + 32
	if temperature_f < 80:
		return ambient_temperature_c

	simple_index = 0.5 * (
		temperature_f
		+ 61.0
		+ ((temperature_f - 68.0) * 1.2)
		+ (relative_humidity * 0.094)
	)
	simple_index = (simple_index + temperature_f) / 2
	if simple_index < 80:
		return ambient_temperature_c

	heat_index_f = (
		-42.379
		+ 2.04901523 * temperature_f
		+ 10.14333127 * relative_humidity
		- 0.22475541 * temperature_f * relative_humidity
		- 0.00683783 * temperature_f**2
		- 0.05481717 * relative_humidity**2
		+ 0.00122874 * temperature_f**2 * relative_humidity
		+ 0.00085282 * temperature_f * relative_humidity**2
		- 0.00000199 * temperature_f**2 * relative_humidity**2
	)

	if relative_humidity < 13 and 80 <= temperature_f <= 112:
		adjustment = ((13 - relative_humidity) / 4) * (
			(17 - abs(temperature_f - 95)) / 17
		) ** 0.5
		heat_index_f -= adjustment
	elif relative_humidity > 85 and 80 <= temperature_f <= 87:
		adjustment = ((relative_humidity - 85) / 10) * ((87 - temperature_f) / 5)
		heat_index_f += adjustment

	return (heat_index_f - 32) * 5 / 9


def classify_heat_index(value_c: float) -> dict:
	if not isfinite(value_c):
		raise ValueError("heat index must be finite")

	value_f = value_c * 9 / 5 + 32
	for lower, upper, category, risk_level, severity in HEAT_INDEX_CATEGORIES:
		if lower <= value_f < upper:
			return {
				"value_c": value_c,
				"value_f": value_f,
				"category": category,
				"risk_level": risk_level,
				"severity": severity,
			}
	return {
		"value_c": value_c,
		"value_f": value_f,
		"category": "no_heat_advisory",
		"risk_level": "low",
		"severity": 0,
	}
