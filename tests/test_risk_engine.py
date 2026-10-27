import pytest

from risk_engine.risk_fusion import evaluate_environmental_risk
from risk_engine.risk_levels import calculate_heat_index_celsius, classify_aqi


@pytest.mark.parametrize(
	("aqi", "category", "risk_level"),
	[
		(50, "good", "low"),
		(51, "moderate", "moderate"),
		(100, "moderate", "moderate"),
		(101, "unhealthy_for_sensitive_groups", "high"),
		(151, "unhealthy", "very_high"),
		(201, "very_unhealthy", "severe"),
		(301, "hazardous", "severe"),
	],
)
def test_classify_aqi_uses_standard_category_breakpoints(aqi, category, risk_level):
	result = classify_aqi(aqi)

	assert result["category"] == category
	assert result["risk_level"] == risk_level


def test_heat_index_matches_expected_hot_humid_reading():
	heat_index_c = calculate_heat_index_celsius(32.2, 70)

	assert heat_index_c == pytest.approx(41.0, abs=0.5)


def test_environmental_risk_uses_highest_available_component():
	result = evaluate_environmental_risk(
		{"aqi": 175, "ambient_temperature": 40, "humidity": 70}
	)

	assert result["risk_level"] == "severe"
	assert result["components"]["air_quality"]["category"] == "unhealthy"
	assert result["components"]["heat"]["severity"] == 4
	assert result["unavailable_inputs"] == []


def test_missing_environmental_inputs_are_reported_as_unknown():
	result = evaluate_environmental_risk(
		{"aqi": None, "ambient_temperature": 30, "humidity": None}
	)

	assert result["risk_level"] == "unknown"
	assert result["severity"] is None
	assert result["components"] == {}
	assert result["unavailable_inputs"] == ["aqi", "heat_index"]


def test_invalid_aqi_is_rejected():
	with pytest.raises(ValueError, match="AQI"):
		evaluate_environmental_risk(
			{"aqi": 1001, "ambient_temperature": 30, "humidity": 50}
		)
