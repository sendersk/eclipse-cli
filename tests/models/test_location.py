"""Tests for the geographic location model."""

import pytest

from eclipse_cli.models.location import Location


def test_location_stores_coordinates() -> None:
    """Verify that a location stores latitude and longitude."""
    location = Location(
        latitude=52.5200,
        longitude=13.4050,
    )

    assert location.latitude == 52.5200
    assert location.longitude == 13.4050


def test_location_is_immutable() -> None:
    """Verify that a location cannot be modified after creation."""
    location = Location(
        latitude=52.5200,
        longitude=13.4050,
    )

    with pytest.raises(AttributeError):
        location.latitude = 50.0
