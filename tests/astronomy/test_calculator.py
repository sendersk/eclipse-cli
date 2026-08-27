"""Tests for astronomical calculations."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from eclipse_cli.astronomy.calculator import AstronomyCalculator
from eclipse_cli.astronomy.models import EphemerisData, CelestialPosition


def create_calculator() -> tuple[AstronomyCalculator, MagicMock]:
    """Create a calculator with a mocked ephemeris."""
    kernel = MagicMock()
    ephemeris = EphemerisData(
        path=MagicMock(),
        kernel=kernel,
    )

    return AstronomyCalculator(ephemeris), kernel


def test_astronomy_calculator_initializes() -> None:
    """Verify that the astronomy calculator initializes."""
    calculator, _ = create_calculator()

    assert calculator is not None


def test_get_sun_position_requires_timezone_aware_datetime() -> None:
    """Verify that a timezone-naive datetime is rejected."""
    calculator, _ = create_calculator()

    timestamp = datetime(2026, 8, 25, 12, 0)

    with pytest.raises(
        ValueError,
        match="Timestamp must be timezone-aware",
    ):
        calculator.get_sun_position(timestamp)


def test_get_sun_position_returns_coordinates() -> None:
    """Verify that the Sun position is returned in degrees."""
    calculator, kernel = create_calculator()

    timescale = MagicMock()
    time = MagicMock()

    right_ascension = MagicMock()
    right_ascension.hours = 10.0

    declination = MagicMock()
    declination.degrees = 20.0

    apparent = MagicMock()
    apparent.radec.return_value = (
        right_ascension,
        declination,
        MagicMock(),
    )

    kernel.timescale.return_value = timescale
    timescale.from_datetime.return_value = time

    earth = MagicMock()
    sun = MagicMock()

    kernel.__getitem__.side_effect = {
        "earth": earth,
        "sun": sun,
    }.__getitem__

    earth.at.return_value.observe.return_value.apparent.return_value = apparent

    timestamp = datetime(
        2026,
        8,
        25,
        12,
        0,
        tzinfo=UTC,
    )

    result = calculator.get_sun_position(timestamp)

    assert result == CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )
    timescale.from_datetime.assert_called_once_with(timestamp)


def test_validate_timestamp_accepts_timezone_aware_datetime() -> None:
    """Verify that timezone-aware datetimes are accepted."""
    timestamp = datetime(
        2026,
        8,
        25,
        12,
        0,
        tzinfo=UTC,
    )

    AstronomyCalculator._validate_timestamp(timestamp)


def test_validate_timestamp_rejects_timezone_naive_datetime() -> None:
    """Verify that timezone-naive datetimes are rejected."""
    timestamp = datetime(2026, 8, 25, 12, 0)

    with pytest.raises(
        ValueError,
        match="Timestamp must be timezone-aware",
    ):
        AstronomyCalculator._validate_timestamp(timestamp)


def test_get_moon_position_returns_coordinates() -> None:
    """Verify that the Moon position is returned in degrees."""
    calculator, kernel = create_calculator()

    timescale = MagicMock()
    time = MagicMock()

    right_ascension = MagicMock()
    right_ascension.hours = 8.0

    declination = MagicMock()
    declination.degrees = -10.0

    apparent = MagicMock()
    apparent.radec.return_value = (
        right_ascension,
        declination,
        MagicMock(),
    )

    kernel.timescale.return_value = timescale
    timescale.from_datetime.return_value = time

    earth = MagicMock()
    moon = MagicMock()

    kernel.__getitem__.side_effect = {
        "earth": earth,
        "moon": moon,
    }.__getitem__

    earth.at.return_value.observe.return_value.apparent.return_value = apparent

    timestamp = datetime(
        2026,
        8,
        25,
        12,
        0,
        tzinfo=UTC,
    )

    result = calculator.get_moon_position(timestamp)

    assert result == CelestialPosition(
        right_ascension=120.0,
        declination=-10.0,
    )
    timescale.from_datetime.assert_called_once_with(timestamp)


def test_calculate_angular_separation_for_same_position() -> None:
    """Verify that identical positions have zero angular separation."""
    position = CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )

    result = AstronomyCalculator.calculate_angular_separation(
        position,
        position,
    )

    assert result == pytest.approx(0.0)


def test_calculate_angular_separation_for_known_positions() -> None:
    """Verify angular separation for two known positions."""
    first = CelestialPosition(
        right_ascension=0.0,
        declination=0.0,
    )
    second = CelestialPosition(
        right_ascension=90.0,
        declination=0.0,
    )

    result = AstronomyCalculator.calculate_angular_separation(
        first,
        second,
    )

    assert result == pytest.approx(90.0)


def test_calculate_angular_separation_uses_declination() -> None:
    """Verify that declination affects angular separation."""
    first = CelestialPosition(
        right_ascension=0.0,
        declination=0.0,
    )
    second = CelestialPosition(
        right_ascension=0.0,
        declination=30.0,
    )

    result = AstronomyCalculator.calculate_angular_separation(
        first,
        second,
    )

    assert result == pytest.approx(30.0)