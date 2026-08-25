"""Services for astronomical calculations."""

from pathlib import Path

from eclipse_cli.astronomy.loader import EphemerisLoader
from eclipse_cli.astronomy.models import EphemerisData
from eclipse_cli.config import AstronomySettings


class AstronomyService:
    """Provide access to astronomical ephemeris data."""

    def __init__(
        self,
        settings: AstronomySettings,
        loader: EphemerisLoader | None = None,
    ) -> None:
        """Initialize the astronomy service."""
        self._settings = settings
        self._loader = loader or EphemerisLoader()

    def load_ephemeris(self) -> EphemerisData:
        """Load the configured astronomical ephemeris.

        Returns:
            Loaded ephemeris data.
        """
        path = Path(self._settings.data_directory) / self._settings.ephemeris
        return self._loader.load(path)