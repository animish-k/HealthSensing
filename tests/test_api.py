from datetime import datetime, timezone

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def payload(**overrides):
    value = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "simulator",
        "scenario": "normal",
        "heart_rate": 72,
        "spo2": 98,
        "body_temperature": 36.8,
        "activity_level": 0.4,
        "ambient_temperature": 28,
        "humidity": 55,
        "aqi": 50,
        "pm25": 12,
    }
    value.update(overrides)
    return value


def test_health_and_reading_endpoints():
    assert client.get("/health").json() == {"status": "ok"}
    response = client.post("/api/readings", json=payload(spo2=None))

    assert response.status_code == 201
    assert response.json()["spo2"] is None
    assert client.get("/api/readings?limit=1").status_code == 200


def test_invalid_reading_is_rejected():
    response = client.post("/api/readings", json=payload(spo2=101))

    assert response.status_code == 422


def test_websocket_receives_persisted_reading():
    with client.websocket_connect("/ws/readings") as websocket:
        response = client.post("/api/readings", json=payload())
        assert response.status_code == 201
        message = websocket.receive_json()
        assert message["source"] == "simulator"
