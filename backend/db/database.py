import sqlite3
from pathlib import Path

from backend.models.measurement import Measurement, MeasurementResponse


class MeasurementRepository:
    """SQLite repository for local measurement storage."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    source TEXT NOT NULL,
                    scenario TEXT,
                    heart_rate REAL,
                    spo2 REAL,
                    body_temperature REAL,
                    activity_level REAL,
                    ambient_temperature REAL,
                    humidity REAL,
                    aqi REAL,
                    pm25 REAL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_measurements_timestamp "
                "ON measurements(timestamp)"
            )

    def add(self, measurement: Measurement) -> MeasurementResponse:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO measurements (
                    timestamp, source, scenario, heart_rate, spo2,
                    body_temperature, activity_level, ambient_temperature,
                    humidity, aqi, pm25
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                measurement.as_storage_tuple(),
            )
            measurement_id = cursor.lastrowid
        return MeasurementResponse(id=measurement_id, **measurement.dict())

    def recent(self, limit: int = 50) -> list[MeasurementResponse]:
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, timestamp, source, scenario, heart_rate, spo2,
                       body_temperature, activity_level, ambient_temperature,
                       humidity, aqi, pm25
                FROM measurements
                ORDER BY timestamp DESC, id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [MeasurementResponse(**dict(row)) for row in rows]