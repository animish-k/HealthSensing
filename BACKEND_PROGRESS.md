# Backend Progress

**Owner:** Vedant Nichal
**Scope:** Backend, shared data interface, persistence, and streaming
**Status:** Backend foundation complete; cross-module integration is ready to begin.

## Completed

### Shared measurement contract

Implemented in [backend/models/measurement.py](backend/models/measurement.py):

- timezone-aware `timestamp`;
- UTC normalization before persistence;
- required `source` provenance;
- optional scenario and sensor/context fields;
- range validation for physiological and environmental values;
- explicit `null` values for unavailable measurements.

The current fields are:

```text
timestamp, source, scenario, heart_rate, spo2, body_temperature,
activity_level, ambient_temperature, humidity, aqi, pm25
```

### Local persistence

Implemented in [backend/db/database.py](backend/db/database.py):

- SQLite database initialization;
- `measurements` table and timestamp index;
- insert and recent-reading retrieval;
- newest-first ordering;
- configurable local path through `HEALTHSENSING_DATABASE_PATH`.

The default database is `data/healthsensing.sqlite3`, which is ignored by Git.

### HTTP API

Implemented in [backend/main.py](backend/main.py) and
[backend/api/routes/current.py](backend/api/routes/current.py):

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/api/readings` | Validate and persist one reading |
| `GET` | `/api/readings?limit=50` | Retrieve recent readings |

Invalid timestamps, blank provenance, out-of-range values, and invalid limits
are rejected by the API.

### WebSocket streaming

Implemented in [backend/websocket/live_stream.py](backend/websocket/live_stream.py)
and [backend/websocket/manager.py](backend/websocket/manager.py):

- dashboard clients connect to `/ws/readings`;
- readings are broadcast only after successful persistence;
- disconnected clients are removed;
- send failures are isolated to the affected client.

### Simulator integration

Implemented in [simulator/data_generator.py](simulator/data_generator.py),
[simulator/simulator.py](simulator/simulator.py), and
[simulator/client.py](simulator/client.py):

- generated records match the backend contract;
- timestamps include timezone information;
- records are marked with `source: "simulator"`;
- finite runs are available for integration tests;
- continuous runs remain available for demonstrations;
- the standard-library client submits readings to the local API and reports
  HTTP/network failures explicitly.

Example:

```python
from simulator.simulator import run_simulator

run_simulator(
    "heatwave",
    count=10,
    endpoint="http://127.0.0.1:8000/api/readings",
)
```

## Tests and validation

Focused tests are available in:

- [tests/test_backend.py](tests/test_backend.py)
- [tests/test_api.py](tests/test_api.py)
- [tests/test_simulator_contract.py](tests/test_simulator_contract.py)

They cover schema validation, optional values, SQLite persistence, ordering,
HTTP ingestion/retrieval, invalid input, finite simulator runs, and WebSocket
delivery.

`git diff --check` passes. The test suite has not run in the current
environment because an installed Python/pytest runtime is unavailable; only
the Microsoft Store Python alias is present.

## Integration contract for the team

- **Animish Kumar:** provide anomaly/baseline outputs for each accepted
  reading. Suggested fields: `anomaly_score`, detector/model name, and
  prediction availability.
- **Avani Asati:** provide risk-fusion output and explanation structure.
  Suggested fields: risk category, severity, triggered rules, contributing
  signals, unavailable inputs, and human-readable explanation.
- **Chaitanya Chalith:** consume `GET /api/readings` for current/history
  views and `/ws/readings` for live updates. Simulated records are identified
  by `source: "simulator"`.
- **Kartikeya Singh:** send cleaned data using the shared measurement fields
  and preserve source/session provenance. Missing fields should remain `null`.
- **Siddhartha Venkata Arava Reddy:** use the same schema when evaluating
  detectors and keep experiment/test-set data separate from simulator
  integration data.
- **Aryan Saini:** use the simulator client or submit generated records to
  `POST /api/readings`; keep simulated data labelled as simulated.

## Remaining work

### Waiting for other modules

1. Add AI anomaly and personal-baseline fields after Animish provides the
   detector interface.
2. Add risk levels, triggered rules, and explanations after Avani provides the
   reasoning/risk-fusion interface.
3. Add dataset-backed evaluation after Kartikeya provides the data inventory
   and Siddhartha provides the evaluation protocol.
4. Connect dashboard cards and charts after Chaitanya confirms the frontend
   API/WebSocket consumption shape.

### Backend-owned follow-up after those interfaces exist

1. Extend the persisted schema for derived anomaly/risk results.
2. Add a service layer that calls detector and risk modules.
3. Add historical risk and alert endpoints.
4. Add WebSocket event types for readings, risk updates, and alerts.
5. Add end-to-end tests across simulator, backend, AI, reasoning, and
   dashboard consumers.

## Run locally

Install [requirements.txt](requirements.txt), then run:

```text
uvicorn backend.main:app --reload
```

Do not commit private wearable exports, raw personal health data, secrets, or
unverified medical claims.
