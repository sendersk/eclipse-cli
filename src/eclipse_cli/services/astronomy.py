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
        self._ephemeris: EphemerisData | None = None

    def load_ephemeris(self) -> EphemerisData:
        """Load the configured astronomical ephemeris.

        Returns:
            Loaded ephemeris data.
        """
        path = Path(self._settings.data_directory) / self._settings.ephemeris

        self._ephemeris = self._loader.load(path)

        return self._ephemeris

    def get_ephemeris(self) -> EphemerisData:
        """Return the loaded astronomical ephemeris.

        Returns:
            Loaded ephemeris data.

        Raises:
            RuntimeError: If the ephemeris has not been loaded yet.
        """
        if self._ephemeris is None:
            raise RuntimeError("Ephemeris has not been loaded.")

        return self._ephemeris
