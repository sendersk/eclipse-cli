"""Domain model for geographic locations."""

from dataclasses import dataclass

from eclipse_cli.models.exceptions import InvalidLocationError

MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0


@dataclass(frozen=True, slots=True)
class Location:
    """Represent a validated geographic location on Earth."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        """Validate geographic coordinates after initialization."""
        self._validate_latitude()
        self._validate_longitude()

    def _validate_latitude(self) -> None:
        """Validate the latitude coordinate."""
        if not MIN_LATITUDE <= self.latitude <= MAX_LATITUDE:
            raise InvalidLocationError(
                f"Latitude must be between {MIN_LATITUDE} and "
                f"{MAX_LATITUDE}, got {self.latitude}.",
            )

    def _validate_longitude(self) -> None:
        """Validate the longitude coordinate."""
        if not MIN_LONGITUDE <= self.longitude <= MAX_LONGITUDE:
            raise InvalidLocationError(
                f"Longitude must be between {MIN_LONGITUDE} and "
                f"{MAX_LONGITUDE}, got {self.longitude}.",
            )
