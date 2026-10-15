from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, validator


class Measurement(BaseModel):
    """A health/environment reading shared by the simulator and backend."""

    timestamp: datetime
    source: str = Field(..., min_length=1, max_length=64)
    scenario: Optional[str] = Field(default=None, max_length=64)
    heart_rate: Optional[float] = Field(default=None, ge=0, le=300)
    spo2: Optional[float] = Field(default=None, ge=0, le=100)
    body_temperature: Optional[float] = Field(default=None, ge=25, le=45)
    activity_level: Optional[float] = Field(default=None, ge=0, le=1)
    ambient_temperature: Optional[float] = Field(default=None, ge=-80, le=80)
    humidity: Optional[float] = Field(default=None, ge=0, le=100)
    aqi: Optional[float] = Field(default=None, ge=0, le=1000)
    pm25: Optional[float] = Field(default=None, ge=0, le=1000)

    @validator("timestamp")
    def timestamp_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must include a timezone offset")
        return value

    @validator("source", "scenario")
    def text_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("text fields must not be blank")
        return value

    def as_storage_tuple(self) -> tuple:
        values = self.dict()
        timestamp = values["timestamp"].astimezone(timezone.utc).isoformat()
        return (
            timestamp,
            values["source"],
            values["scenario"],
            values["heart_rate"],
            values["spo2"],
            values["body_temperature"],
            values["activity_level"],
            values["ambient_temperature"],
            values["humidity"],
            values["aqi"],
            values["pm25"],
        )


class MeasurementResponse(Measurement):
    id: int