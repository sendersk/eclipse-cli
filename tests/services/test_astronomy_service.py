"""Tests for the astronomy service."""

from pathlib import Path
from unittest.mock import MagicMock

from eclipse_cli.config import AstronomySettings
from eclipse_cli.services.astronomy import AstronomyService


def create_settings(tmp_path: Path) -> AstronomySettings:
    """Create valid astronomy settings for tests."""
    return AstronomySettings(
        data_directory=tmp_path,
        ephemeris="de440.bsp",
    )


def test_astronomy_service_initializes(
    tmp_path: Path,
) -> None:
    """Verify that the astronomy service initializes successfully."""
    settings = create_settings(tmp_path)

    service = AstronomyService(settings)

    assert service is not None


def test_astronomy_service_loads_configured_ephemeris(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Verify that the configured ephemeris is loaded."""
    expected_ephemeris = MagicMock()
    loader = MagicMock(return_value=expected_ephemeris)
    loader_factory = MagicMock(return_value=loader)

    monkeypatch.setattr(
        "eclipse_cli.services.astronomy.Loader",
        loader_factory,
    )

    settings = create_settings(tmp_path)

    service = AstronomyService(settings)
    result = service.load_ephemeris()

    assert result is expected_ephemeris
    loader_factory.assert_called_once_with(tmp_path)
    loader.assert_called_once_with("de440.bsp")