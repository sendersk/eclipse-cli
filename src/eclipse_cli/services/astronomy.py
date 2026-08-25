"""Services for astronomical calculations."""

from typing import Any

from skyfield.api import Loader

from eclipse_cli.config import AstronomySettings


class AstronomyService:
    """Provide access to astronomical ephemeris data."""

    def __init__(self, settings: AstronomySettings) -> None:
        """Initialize the astronomy service."""
        self._settings = settings
        self._loader = Loader(settings.data_directory)

    def load_ephemeris(self) -> Any:
        """Load the configured astronomical ephemeris file."""
        return self._loader(self._settings.ephemeris)