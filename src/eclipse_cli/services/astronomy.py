"""Services for astronomical calculations."""

from skyfield.api import Loader
from typing import Any


class AstronomyService:
    """Provide access to astronomical ephemeris data."""

    def __init__(self, data_directory: str) -> None:
        """Initialize the astronomy service."""
        self._loader = Loader(data_directory)

    def load_ephemeris(self, filename: str) -> Any:
        """Load an astronomical ephemeris file."""
        return self._loader(filename)