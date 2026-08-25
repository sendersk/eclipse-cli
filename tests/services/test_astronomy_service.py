"""Tests for the astronomy service."""

from pathlib import Path
from unittest.mock import MagicMock

from eclipse_cli.services.astronomy import AstronomyService


def test_astronomy_service_initializes_with_data_directory(
    tmp_path: Path,
) -> None:
    """Verify that the astronomy service accepts a data directory."""
    service = AstronomyService(tmp_path)

    assert service is not None


def test_astronomy_service_loads_ephemeris(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Verify that the astronomy service loads an ephemeris file."""
    expected_ephemeris = MagicMock()
    loader = MagicMock(return_value=expected_ephemeris)

    monkeypatch.setattr(
        "eclipse_cli.services.astronomy.Loader",
        MagicMock(return_value=loader),
    )

    service = AstronomyService(tmp_path)

    result = service.load_ephemeris("de440.bsp")

    assert result is expected_ephemeris
    loader.assert_called_once_with("de440.bsp")