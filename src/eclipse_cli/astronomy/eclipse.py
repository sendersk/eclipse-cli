"""Eclipse calculation utilities."""

from datetime import datetime

from eclipse_cli.astronomy.calculator import AstronomyCalculator
from eclipse_cli.astronomy.models import CelestialPosition


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