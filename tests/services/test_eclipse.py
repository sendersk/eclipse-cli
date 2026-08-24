"""Tests for the eclipse service."""

from eclipse_cli.models.location import Location
from eclipse_cli.services.eclipse import EclipseService


def test_calculate_accepts_location() -> None:
    """Verify that the eclipse service accepts a geographic location."""
    service = EclipseService()
    location = Location(
        latitude=52.5200,
        longitude=13.4050,
    )

    result = service.calculate(location)

    assert result is None