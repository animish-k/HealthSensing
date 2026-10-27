def build_explanation(
	risk_level: str,
	components: dict,
	unavailable_inputs: list[str],
) -> str:
	if risk_level == "unknown":
		return "Environmental risk could not be assessed from the available inputs."

	drivers = [
		name.replace("_", " ")
		for name, result in components.items()
		if result["severity"] > 0 and result["risk_level"] == risk_level
	]
	if drivers:
		summary = (
			f"Environmental screening is {risk_level.replace('_', ' ')}; "
			f"the highest contributing signal is {', '.join(drivers)}."
		)
	else:
		summary = "Available environmental inputs indicate a low screening level."

	if unavailable_inputs:
		missing = ", ".join(value.replace("_", " ") for value in unavailable_inputs)
		summary += f" Not assessed: {missing}."
	return summary
