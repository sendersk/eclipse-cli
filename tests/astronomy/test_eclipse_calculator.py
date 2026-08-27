"""Tests for eclipse calculations."""

from unittest.mock import MagicMock

import pytest

from eclipse_cli.astronomy.calculator import AstronomyCalculator
from eclipse_cli.astronomy.eclipse import EclipseCalculator
from eclipse_cli.astronomy.models import CelestialPosition


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