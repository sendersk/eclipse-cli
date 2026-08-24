"""Astronomical data models."""

from dataclasses import dataclass
from pathlib import Path

from skyfield.jpllib import SpiceKernel


@dataclass(frozen=True, slots=True)
class EphemerisData:
    """Represent loaded JPL ephemeris data."""

    path: Path
    kernel: SpiceKernel
