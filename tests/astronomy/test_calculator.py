"""Tests for astronomical calculations."""

from unittest.mock import MagicMock

from eclipse_cli.astronomy.calculator import AstronomyCalculator


def test_astronomy_calculator_initializes() -> None:
    """Verify that the astronomy calculator initializes."""
    ephemeris = MagicMock()

    calculator = AstronomyCalculator(ephemeris)

    assert calculator is not None