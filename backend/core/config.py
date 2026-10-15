from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "healthsensing.sqlite3"


def database_path() -> Path:
    """Return the configured local database path."""
    return Path(os.getenv("HEALTHSENSING_DATABASE_PATH", str(DEFAULT_DATABASE_PATH)))