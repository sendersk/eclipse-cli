"""Domain model for geographic locations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Location:
    """Represent a geographic location on Earth."""

    latitude: float
    longitude: float
