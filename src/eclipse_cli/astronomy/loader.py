"""JPL ephemeris data loader."""

from pathlib import Path

from skyfield.api import load
from skyfield.jpllib import SpiceKernel

from eclipse_cli.astronomy.exceptions import EphemerisError
from eclipse_cli.astronomy.models import EphemerisData


class EphemerisLoader:
    """Load JPL ephemeris data from a local file."""

    def load(self, path: Path) -> EphemerisData:
        """Load an ephemeris file.

        Args:
            path: Path to the JPL ephemeris file.

        Returns:
            Loaded ephemeris data.

        Raises:
            EphemerisError: If the ephemeris file cannot be loaded.
        """
        self._validate_path(path)

        try:
            kernel = load_file(path)
        except Exception as error:
            raise EphemerisError(f"Unable to load ephemeris file: {path}") from error

        return EphemerisData(
            path=path,
            kernel=kernel,
        )

    @staticmethod
    def _validate_path(path: Path) -> None:
        """Validate the ephemeris file path.

        Args:
            path: Path to the ephemeris file.

        Raises:
            EphemerisError: If the path does not point to a file.
        """
        if not path.exists():
            raise EphemerisError(f"Ephemeris file does not exist: {path}")

        if not path.is_file():
            raise EphemerisError(f"Ephemeris path is not a file: {path}")


def load_file(path: Path) -> SpiceKernel:
    """Load a JPL ephemeris file with Skyfield.

    Args:
        path: Path to the ephemeris file.

    Returns:
        Loaded Skyfield kernel.
    """
    return load(path)
