"""Tests for the location service."""

import pytest

from eclipse_cli.models.exceptions import InvalidLocationError
from eclipse_cli.models.location import Location
from eclipse_cli.services.location import LocationService


def test_create_location_returns_location() -> None:
    """Verify that the service creates a location."""
    service = LocationService()

    location = service.create_location(
        latitude=52.5200,
        longitude=13.4050,
    )

    assert location == Location(
        latitude=52.5200,
        longitude=13.4050,
    )


@pytest.mark.parametrize(
    ("latitude", "longitude"),
    [
        (-90.0, -180.0),
        (90.0, 180.0),
        (0.0, 0.0),
    ],
)
def test_create_location_accepts_valid_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """Verify that the service accepts valid coordinates."""
    service = LocationService()

    location = service.create_location(
        latitude=latitude,
        longitude=longitude,
    )

    assert location.latitude == latitude
    assert location.longitude == longitude


def test_create_location_rejects_invalid_latitude() -> None:
    """Verify that the service rejects invalid latitude."""
    service = LocationService()

    with pytest.raises(InvalidLocationError):
        service.create_location(
            latitude=91.0,
            longitude=0.0,
        )


def test_create_location_rejects_invalid_longitude() -> None:
    """Verify that the service rejects invalid longitude."""
    service = LocationService()

    with pytest.raises(InvalidLocationError):
        service.create_location(
            latitude=0.0,
            longitude=181.0,
        )
