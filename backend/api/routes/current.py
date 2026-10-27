from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder

from backend.db.database import MeasurementRepository
from backend.models.measurement import Measurement, MeasurementResponse
from backend.websocket.live_stream import manager


router = APIRouter(prefix="/readings", tags=["readings"])


def get_repository() -> MeasurementRepository:
    raise RuntimeError("The repository dependency is not configured")


@router.post("", response_model=MeasurementResponse, status_code=201)
async def ingest_reading(
    measurement: Measurement,
    repository: MeasurementRepository = Depends(get_repository),
) -> MeasurementResponse:
    saved = repository.add(measurement)
    await manager.broadcast(jsonable_encoder(saved))
    return saved


@router.get("", response_model=list[MeasurementResponse])
def list_readings(
    limit: int = Query(default=50, ge=1, le=500),
    repository: MeasurementRepository = Depends(get_repository),
) -> list[MeasurementResponse]:
    return repository.recent(limit)