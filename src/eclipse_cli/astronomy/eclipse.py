"""Eclipse calculation utilities."""

from datetime import datetime

from eclipse_cli.astronomy.calculator import AstronomyCalculator
from eclipse_cli.astronomy.models import CelestialPosition, EclipseResult

ECLIPSE_SEPARATION_THRESHOLD_DEGREES = 1.0


class EclipseCalculator:
    """Determine whether celestial positions indicate an eclipse."""

    def __init__(
        self,
        astronomy_calculator: AstronomyCalculator,
    ) -> None:
        """Initialize the eclipse calculator."""
        self._astronomy = astronomy_calculator

    def calculate_separation(
        self,
        sun_position: CelestialPosition,
        moon_position: CelestialPosition,
    ) -> float:
        """
        Calculate the angular separation between the Sun and Moon.

        Args:
            sun_position: Apparent Sun position.
            moon_position: Apparent Moon position.

        Returns:
            Angular separation in degrees.
        """
        return self._astronomy.calculate_angular_separation(
            sun_position,
            moon_position,
        )

    def calculate_positions(
        self,
        timestamp: datetime,
    ) -> tuple[CelestialPosition, CelestialPosition]:
        """
        Calculate the apparent positions of the Sun and Moon.

        Args:
            timestamp: Timestamp for the calculation.

        Returns:
            Tuple containing Sun position and Moon position.
        """
        sun_position = self._astronomy.get_sun_position(timestamp)
        moon_position = self._astronomy.get_moon_position(timestamp)

        return sun_position, moon_position

    def calculate_angular_separation(
        self,
        timestamp: datetime,
    ) -> float:
        """
        Calculate the angular separation between the Sun and Moon.

        Args:
            timestamp: Timestamp for the calculation.

        Returns:
            Angular separation in degrees.
        """
        sun_position, moon_position = self.calculate_positions(timestamp)

        return self.calculate_separation(
            sun_position,
            moon_position,
        )

    @staticmethod
    def is_eclipse_candidate(
        result: EclipseResult,
    ) -> bool:
        """Determine whether a calculation result is an eclipse candidate."""
        return (
            result.angular_separation
            <= ECLIPSE_SEPARATION_THRESHOLD_DEGREES
        )

    def calculate(
        self,
        timestamp: datetime,
    ) -> EclipseResult:
        """
        Calculate the complete eclipse result for a timestamp.

        Args:
            timestamp: Timestamp for the calculation.

        Returns:
            Complete eclipse calculation result.
        """
        sun_position, moon_position = self.calculate_positions(timestamp)

        angular_separation = self.calculate_separation(
            sun_position,
            moon_position,
        )

        result = EclipseResult(
            timestamp=timestamp,
            sun_position=sun_position,
            moon_position=moon_position,
            angular_separation=angular_separation,
        )

        return EclipseResult(
            timestamp=result.timestamp,
            sun_position=result.sun_position,
            moon_position=result.moon_position,
            angular_separation=result.angular_separation,
            is_eclipse=self.is_eclipse_candidate(result),
        )