"""Eclipse calculation utilities."""

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