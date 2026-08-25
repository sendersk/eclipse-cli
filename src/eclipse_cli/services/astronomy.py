"""Services for astronomical calculations."""

from skyfield.api import Loader
from skyfield.jpllib import SpiceKernel

from eclipse_cli.config import AstronomySettings
from eclipse_cli.models.exceptions import EphemerisError


class AstronomyService:
    """Provide access to astronomical ephemeris data."""

    def __init__(self, settings: AstronomySettings) -> None:
        """Initialize the astronomy service."""
        self._settings = settings
        self._loader = Loader(settings.data_directory)

    def load_ephemeris(self) -> SpiceKernel:
        """
        Load the configured astronomical ephemeris.

        Returns:
            Loaded Skyfield ephemeris.

        Raises:
            EphemerisError: If the ephemeris cannot be loaded.
        """
        try:
            return self._loader(self._settings.ephemeris)
        except (OSError, ValueError) as error:
            raise EphemerisError(
                f"Unable to load ephemeris: {self._settings.ephemeris}"
            ) from error