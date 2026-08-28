"""Tests for eclipse calculations."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from eclipse_cli.astronomy.calculator import AstronomyCalculator
from eclipse_cli.astronomy.eclipse import EclipseCalculator
from eclipse_cli.astronomy.models import CelestialPosition, EclipseResult

ECLIPSE_SEPARATION_THRESHOLD_DEGREES = 1.0


def test_eclipse_calculator_initializes() -> None:
    """Verify that the eclipse calculator initializes."""
    astronomy_calculator = MagicMock(spec=AstronomyCalculator)

    calculator = EclipseCalculator(astronomy_calculator)

    assert calculator is not None


def test_calculate_separation_delegates_to_astronomy_calculator() -> None:
    """Verify that angular separation is delegated correctly."""
    astronomy_calculator = MagicMock(spec=AstronomyCalculator)

    sun_position = CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )
    moon_position = CelestialPosition(
        right_ascension=151.0,
        declination=20.5,
    )

    astronomy_calculator.calculate_angular_separation.return_value = 0.5

    calculator = EclipseCalculator(astronomy_calculator)

    result = calculator.calculate_separation(
        sun_position,
        moon_position,
    )

    assert result == pytest.approx(0.5)

    astronomy_calculator.calculate_angular_separation.assert_called_once_with(
        sun_position,
        moon_position,
    )


def test_calculate_positions_returns_sun_and_moon_positions() -> None:
    """Verify that Sun and Moon positions are calculated."""
    astronomy_calculator = MagicMock(spec=AstronomyCalculator)

    sun_position = CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )
    moon_position = CelestialPosition(
        right_ascension=151.0,
        declination=20.5,
    )

    astronomy_calculator.get_sun_position.return_value = sun_position
    astronomy_calculator.get_moon_position.return_value = moon_position

    calculator = EclipseCalculator(astronomy_calculator)

    timestamp = datetime(
        2026,
        8,
        25,
        12,
        0,
        tzinfo=UTC,
    )

    result = calculator.calculate_positions(timestamp)

    assert result == (sun_position, moon_position)

    astronomy_calculator.get_sun_position.assert_called_once_with(timestamp)
    astronomy_calculator.get_moon_position.assert_called_once_with(timestamp)


def test_calculate_angular_separation_uses_positions() -> None:
    """Verify that angular separation uses calculated positions."""
    astronomy_calculator = MagicMock(spec=AstronomyCalculator)

    sun_position = CelestialPosition(
        right_ascension=150.0,
        declination=20.0,
    )
    moon_position = CelestialPosition(
        right_ascension=151.0,
        declination=20.5,
    )

    astronomy_calculator.get_sun_position.return_value = sun_position
    astronomy_calculator.get_moon_position.return_value = moon_position
    astronomy_calculator.calculate_angular_separation.return_value = 0.75

    calculator = EclipseCalculator(astronomy_calculator)

    timestamp = datetime(
        2026,
        8,
        25,
        12,
        0,
        tzinfo=UTC,
    )

    result = calculator.calculate_angular_separation(timestamp)

    assert result == pytest.approx(0.75)

    astronomy_calculator.get_sun_position.assert_called_once_with(timestamp)
    astronomy_calculator.get_moon_position.assert_called_once_with(timestamp)


def test_is_eclipse_candidate_returns_true_at_threshold() -> None:
    """Verify that the threshold itself is considered a candidate."""
    result = EclipseResult(
        timestamp=datetime(
            2026,
            8,
            25,
            12,
            0,
            tzinfo=UTC,
        ),
        sun_position=CelestialPosition(
            right_ascension=150.0,
            declination=20.0,
        ),
        moon_position=CelestialPosition(
            right_ascension=151.0,
            declination=20.5,
        ),
        angular_separation=1.0,
    )

    assert EclipseCalculator.is_eclipse_candidate(result) is True


def test_calculate_returns_eclipse_result() -> None:
    """Verify that a complete calculation returns an EclipseResult."""
    astronomy_calculator = MagicMock()
    calculator = EclipseCalculator(astronomy_calculator)

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
        right_ascension=151.0,
        declination=20.5,
    )

    astronomy_calculator.get_sun_position.return_value = sun_position
    astronomy_calculator.get_moon_position.return_value = moon_position
    astronomy_calculator.calculate_angular_separation.return_value = 0.8

    result = calculator.calculate(timestamp)

    assert isinstance(result, EclipseResult)
    assert result.timestamp == timestamp
    assert result.sun_position == sun_position
    assert result.moon_position == moon_position
    assert result.angular_separation == 0.8

    astronomy_calculator.get_sun_position.assert_called_once_with(timestamp)
    astronomy_calculator.get_moon_position.assert_called_once_with(timestamp)
    astronomy_calculator.calculate_angular_separation.assert_called_once_with(
        sun_position,
        moon_position,
    )


def test_is_eclipse_candidate_returns_true_within_threshold() -> None:
    """Verify that a result within the threshold is an eclipse candidate."""
    result = EclipseResult(
        timestamp=datetime(
            2026,
            8,
            25,
            12,
            0,
            tzinfo=UTC,
        ),
        sun_position=CelestialPosition(
            right_ascension=150.0,
            declination=20.0,
        ),
        moon_position=CelestialPosition(
            right_ascension=151.0,
            declination=20.5,
        ),
        angular_separation=0.8,
    )

    assert EclipseCalculator.is_eclipse_candidate(result) is True


def test_is_eclipse_candidate_returns_false_above_threshold() -> None:
    """Verify that a result above the threshold is not an eclipse candidate."""
    result = EclipseResult(
        timestamp=datetime(
            2026,
            8,
            25,
            12,
            0,
            tzinfo=UTC,
        ),
        sun_position=CelestialPosition(
            right_ascension=150.0,
            declination=20.0,
        ),
        moon_position=CelestialPosition(
            right_ascension=151.0,
            declination=20.5,
        ),
        angular_separation=1.1,
    )

    assert EclipseCalculator.is_eclipse_candidate(result) is False


def test_calculate_result_can_be_evaluated_as_eclipse_candidate() -> None:
    """Verify that a calculated result can be evaluated as an eclipse candidate."""
    astronomy_calculator = MagicMock()
    calculator = EclipseCalculator(astronomy_calculator)

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
        right_ascension=150.5,
        declination=20.2,
    )

    astronomy_calculator.get_sun_position.return_value = sun_position
    astronomy_calculator.get_moon_position.return_value = moon_position
    astronomy_calculator.calculate_angular_separation.return_value = 0.8

    result = calculator.calculate(timestamp)

    assert result.angular_separation == 0.8
    assert EclipseCalculator.is_eclipse_candidate(result) is True


def test_calculate_result_can_be_rejected_as_eclipse_candidate() -> None:
    """Verify that a calculated result can be rejected as an eclipse candidate."""
    astronomy_calculator = MagicMock()
    calculator = EclipseCalculator(astronomy_calculator)

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
        right_ascension=155.0,
        declination=25.0,
    )

    astronomy_calculator.get_sun_position.return_value = sun_position
    astronomy_calculator.get_moon_position.return_value = moon_position
    astronomy_calculator.calculate_angular_separation.return_value = 5.0

    result = calculator.calculate(timestamp)

    assert result.angular_separation == 5.0
    assert EclipseCalculator.is_eclipse_candidate(result) is False
