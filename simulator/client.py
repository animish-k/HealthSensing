import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class IngestionError(RuntimeError):
    """Raised when the simulator cannot submit a reading."""


def post_reading(
    reading: dict[str, Any],
    endpoint: str = "http://127.0.0.1:8000/api/readings",
    timeout: float = 5,
) -> dict[str, Any]:
    """Submit one generated reading to the local backend."""
    request = Request(
        endpoint,
        data=json.dumps(reading).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise IngestionError(
            f"Backend rejected reading with HTTP {error.code}: {detail}"
        ) from error
    except URLError as error:
        raise IngestionError(f"Backend is unavailable: {error.reason}") from error
