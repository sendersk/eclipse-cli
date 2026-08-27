"""Astronomical calculation utilities."""

from datetime import UTC, datetime
from math import acos, cos, degrees, radians, sin

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

    def get_moon_position(
            self,
            timestamp: datetime,
    ) -> CelestialPosition:
        """
        Calculate the apparent position of the Moon.

        Args:
            timestamp: UTC datetime for the calculation.

        Returns:
            Apparent Moon position as celestial coordinates.

        Raises:
            ValueError: If the timestamp is not timezone-aware.
        """
        self._validate_timestamp(timestamp)

        utc_timestamp = timestamp.astimezone(UTC)

        timescale = self._ephemeris.kernel.timescale()
        time = timescale.from_datetime(utc_timestamp)

        earth = self._ephemeris.kernel["earth"]
        moon = self._ephemeris.kernel["moon"]

        apparent = earth.at(time).observe(moon).apparent()
        right_ascension, declination, _ = apparent.radec()

        return CelestialPosition(
            right_ascension=right_ascension.hours * 15.0,
            declination=declination.degrees,
        )

    @staticmethod
    def calculate_angular_separation(
            first: CelestialPosition,
            second: CelestialPosition,
    ) -> float:
        """
        Calculate the angular separation between two celestial positions.

        Args:
            first: First celestial position.
            second: Second celestial position.

        Returns:
            Angular separation in degrees.
        """
        first_ra = radians(first.right_ascension)
        second_ra = radians(second.right_ascension)

        first_dec = radians(first.declination)
        second_dec = radians(second.declination)

        cosine = (
                sin(first_dec) * sin(second_dec)
                + cos(first_dec)
                * cos(second_dec)
                * cos(first_ra - second_ra)
        )

        # Protect against floating-point rounding outside [-1, 1].
        cosine = max(-1.0, min(1.0, cosine))

        return degrees(acos(cosine))