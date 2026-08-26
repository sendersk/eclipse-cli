"""Astronomical calculation utilities."""

from datetime import UTC, datetime

from eclipse_cli.astronomy.models import EphemerisData, CelestialPosition


class AstronomyCalculator:
    """Perform astronomical calculations using ephemeris data."""

    def __init__(self, ephemeris: EphemerisData) -> None:
        """Initialize the calculator with ephemeris data."""
        self._ephemeris = ephemeris

    def get_sun_position(
            self,
            timestamp: datetime,
    ) -> CelestialPosition:
        """
        Calculate the apparent position of the Sun.

        Args:
            timestamp: UTC datetime for the calculation.

        Returns:
            Apparent Sun position as celestial coordinates.

        Raises:
            ValueError: If the timestamp is not timezone-aware.
        """
        self._validate_timestamp(timestamp)

        utc_timestamp = timestamp.astimezone(UTC)

        timescale = self._ephemeris.kernel.timescale()
        time = timescale.from_datetime(utc_timestamp)

        earth = self._ephemeris.kernel["earth"]
        sun = self._ephemeris.kernel["sun"]

        apparent = earth.at(time).observe(sun).apparent()
        right_ascension, declination, _ = apparent.radec()

        return CelestialPosition(
            right_ascension=right_ascension.hours * 15.0,
            declination=declination.degrees,
        )

    @staticmethod
    def _validate_timestamp(timestamp: datetime) -> None:
        """Validate an astronomical calculation timestamp."""
        if timestamp.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware.")