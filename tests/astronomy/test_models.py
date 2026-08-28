"""Tests for astronomy data models."""

from pathlib import Path
from datetime import datetime, UTC

import pytest
from skyfield.jpllib import SpiceKernel

from eclipse_cli.astronomy.models import CelestialPosition, EphemerisData, EclipseResult


def test_ephemeris_data_stores_path_and_kernel() -> None:
    """Verify that ephemeris data stores its path and kernel."""
    kernel = SpiceKernel.__new__(SpiceKernel)
    path = Path("data/ephemeris/de440.bsp")

    data = EphemerisData(
        path=path,
        kernel=kernel,
    )

    assert data.path == path
    assert data.kernel is kernel


def test_ephemeris_data_is_immutable() -> None:
    """Verify that ephemeris data cannot be modified."""
    kernel = SpiceKernel.__new__(SpiceKernel)

    data = EphemerisData(
        path=Path("data/ephemeris/de440.bsp"),
        kernel=kernel,
    )

    with pytest.raises(AttributeError):
        data.path = Path("other.bsp")


def test_celestial_position_stores_coordinates() -> None:
    """Verify that celestial coordinates are stored correctly."""
    position = CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )

    assert position.right_ascension == 150.0
    assert position.declination == 20.0


def test_eclipse_result_stores_calculation_result() -> None:
    """Verify that EclipseResult stores all calculated values."""
    timestamp = datetime(
        2026,
        8,
        25,
        12,
        0,
        tzinfo=UTC,
    )

    sun_position = CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )
    moon_position = CelestialPosition(
        right_ascension=151.5,
        declination=21.0,
    )

    result = EclipseResult(
        timestamp=timestamp,
        sun_position=sun_position,
        moon_position=moon_position,
        angular_separation=1.8,
    )

    assert result.timestamp == timestamp
    assert result.sun_position == sun_position
    assert result.moon_position == moon_position
    assert result.angular_separation == 1.8