"""Astronomical calculation utilities."""

from skyfield.jpllib import SpiceKernel


class AstronomyCalculator:
    """Perform astronomical calculations using an ephemeris."""

    def __init__(self, ephemeris: SpiceKernel) -> None:
        """Initialize the calculator with an ephemeris."""
        self._ephemeris = ephemeris