from fastapi import FastAPI

from backend.api.routes import current, health
from backend.api.routes.current import get_repository
from backend.core.config import database_path
from backend.db.database import MeasurementRepository
from backend.websocket.live_stream import router as live_stream_router


repository = MeasurementRepository(database_path())
repository.initialize()

app = FastAPI(
    title="HealthSensing API",
    description="Local-first health and environmental reading service.",
    version="0.1.0",
)
app.dependency_overrides[get_repository] = lambda: repository
app.include_router(health.router)
app.include_router(current.router, prefix="/api")
app.include_router(live_stream_router)