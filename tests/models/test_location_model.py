"""Tests for the geographic location model."""

import pytest

from eclipse_cli.models.exceptions import InvalidLocationError
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


@pytest.mark.parametrize(
    ("latitude", "longitude"),
    [
        (-90.0, -180.0),
        (-90.0, 180.0),
        (90.0, -180.0),
        (90.0, 180.0),
        (0.0, 0.0),
        (52.5200, 13.4050),
    ],
)
def test_location_accepts_valid_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """Verify that valid geographic coordinates are accepted."""
    location = Location(
        latitude=latitude,
        longitude=longitude,
    )

    assert location.latitude == latitude
    assert location.longitude == longitude


@pytest.mark.parametrize(
    "latitude",
    [-90.1, 90.1, -180.0, 180.0],
)
def test_location_rejects_invalid_latitude(latitude: float) -> None:
    """Verify that invalid latitude values are rejected."""
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=latitude,
            longitude=0.0,
        )


@pytest.mark.parametrize(
    "longitude",
    [-180.1, 180.1, -360.0, 360.0],
)
def test_location_rejects_invalid_longitude(longitude: float) -> None:
    """Verify that invalid longitude values are rejected."""
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=0.0,
            longitude=longitude,
        )


def test_invalid_latitude_error_contains_value() -> None:
    """Verify that invalid latitude errors contain the invalid value."""
    with pytest.raises(
        InvalidLocationError,
        match=r"Latitude must be between -90\.0 and 90\.0, got 91\.0\.",
    ):
        Location(
            latitude=91.0,
            longitude=0.0,
        )


def test_invalid_longitude_error_contains_value() -> None:
    """Verify that invalid longitude errors contain the invalid value."""
    with pytest.raises(
        InvalidLocationError,
        match=r"Longitude must be between -180\.0 and 180\.0, got 181\.0\.",
    ):
        Location(
            latitude=0.0,
            longitude=181.0,
        )
