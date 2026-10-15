# HealthSensing

HealthSensing is a local-first personal health analytics prototype for
personalized metrics and early warnings about environmental health risks. It
is a risk-screening project, not a medical diagnostic system.

## Current progress

The repository is starting from a scaffold. The first implemented vertical
slice is the backend contract and local persistence:

- validated health/environment measurements with explicit source provenance;
- timezone-aware timestamps normalized to UTC for storage;
- SQLite persistence for recent readings;
- `GET /health`, `POST /api/readings`, and `GET /api/readings`.

The task brief assigns Vedant Nichal ownership of backend, data interface,
persistence, and streaming. The execution order is:

1. Freeze the shared measurement contract.
2. Add SQLite persistence and the minimal ingestion/retrieval API.
3. Connect the seeded simulator to the ingestion endpoint.
4. Add risk/module response fields and transparent rule outputs.
5. Add WebSocket live updates and dashboard integration.
6. Test invalid input, missing optional fields, disconnected clients, and
   persistence before expanding the API.

## Run the backend locally

Install dependencies from `requirements.txt`, then run:

```text
uvicorn backend.main:app --reload
```

The default database is `data/healthsensing.sqlite3`. Set
`HEALTHSENSING_DATABASE_PATH` to use another local path. Do not commit raw
wearable exports, secrets, or other sensitive health data.

The simulator can run a finite integration stream and submit records to the
local API from Python:

```python
from simulator.simulator import run_simulator

run_simulator(
    "heatwave",
    count=10,
    endpoint="http://127.0.0.1:8000/api/readings",
)
```

Dashboard clients can subscribe to `ws://127.0.0.1:8000/ws/readings`.
Each persisted reading is broadcast only after the database insert succeeds.

See [BACKEND_PROGRESS.md](BACKEND_PROGRESS.md) for the detailed implementation
status, integration contract, team dependencies, and remaining work.