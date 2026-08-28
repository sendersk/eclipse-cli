"""Astronomical calculation utilities."""

from datetime import UTC, datetime
from math import acos, cos, degrees, radians, sin

from eclipse_cli.astronomy.models import CelestialPosition, EphemerisData, EclipseResult


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

    def calculate_positions(
            self,
            timestamp: datetime,
    ) -> tuple[CelestialPosition, CelestialPosition]:
        """Calculate the apparent positions of the Sun and Moon."""
        sun_position = self.get_sun_position(timestamp)
        moon_position = self.get_moon_position(timestamp)

        return sun_position, moon_position

    @staticmethod
    def calculate_separation(
            sun_position: CelestialPosition,
            moon_position: CelestialPosition,
    ) -> float:
        """Calculate the angular separation between the Sun and Moon."""
        return AstronomyCalculator.calculate_angular_separation(
            sun_position,
            moon_position,
        )

    def calculate_eclipse_result(
            self,
            timestamp: datetime,
    ) -> EclipseResult:
        """
        Calculate the complete eclipse-related result for a timestamp.

        Args:
            timestamp: Datetime for the calculation.

        Returns:
            Calculated eclipse result containing both celestial positions
            and their angular separation.
        """
        sun_position, moon_position = self.calculate_positions(timestamp)

        angular_separation = self.calculate_separation(
            sun_position,
            moon_position,
        )

        return EclipseResult(
            timestamp=timestamp,
            sun_position=sun_position,
            moon_position=moon_position,
            angular_separation=angular_separation,
        )

    def calculate(self, timestamp: datetime) -> EclipseResult:
        """
        Calculate the astronomical state for a given timestamp.

        Args:
            timestamp: Time of the calculation.

        Returns:
            Complete eclipse calculation result.
        """
        sun_position, moon_position = self.calculate_positions(timestamp)

        angular_separation = self.calculate_separation(
            sun_position,
            moon_position,
        )

        return EclipseResult(
            timestamp=timestamp,
            sun_position=sun_position,
            moon_position=moon_position,
            angular_separation=angular_separation,
        )