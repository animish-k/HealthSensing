"""Database schema entry point kept separate for future migrations."""

from backend.db.database import MeasurementRepository


def initialize_database(repository: MeasurementRepository) -> None:
    repository.initialize()