"""Services for working with geographic locations."""

from eclipse_cli.models.location import Location


class LocationService:
    """Provide operations related to geographic locations."""

    def create_location(self, latitude: float, longitude: float) -> Location:
        """Create a validated geographic location."""
        return Location(
            latitude=latitude,
            longitude=longitude,
        )
