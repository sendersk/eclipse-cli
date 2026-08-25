"""Tests for the astronomy service."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from eclipse_cli.astronomy.loader import EphemerisLoader
from eclipse_cli.astronomy.models import EphemerisData
from eclipse_cli.config import AstronomySettings
from eclipse_cli.services.astronomy import AstronomyService


def create_settings(tmp_path: Path) -> AstronomySettings:
    """Create astronomy settings for testing."""
    return AstronomySettings(
        data_directory=tmp_path,
        ephemeris="de440.bsp",
    )


def test_astronomy_service_initializes(tmp_path: Path) -> None:
    """Verify that the astronomy service initializes successfully."""
    settings = create_settings(tmp_path)

    service = AstronomyService(settings)

    assert service is not None


def test_astronomy_service_loads_configured_ephemeris(
    tmp_path: Path,
) -> None:
    """Verify that the configured ephemeris is loaded."""
    settings = create_settings(tmp_path)

    expected_data = MagicMock(spec=EphemerisData)

    loader = MagicMock(spec=EphemerisLoader)
    loader.load.return_value = expected_data

    service = AstronomyService(
        settings,
        loader=loader,
    )

    result = service.load_ephemeris()

    assert result is expected_data
    loader.load.assert_called_once_with(
        tmp_path / "de440.bsp",
    )


def test_get_ephemeris_returns_loaded_data(
    tmp_path: Path,
) -> None:
    """Verify that loaded ephemeris data can be retrieved."""
    settings = create_settings(tmp_path)

    expected_data = MagicMock(spec=EphemerisData)

    loader = MagicMock(spec=EphemerisLoader)
    loader.load.return_value = expected_data

    service = AstronomyService(
        settings,
        loader=loader,
    )

    service.load_ephemeris()

    result = service.get_ephemeris()

    assert result is expected_data


def test_get_ephemeris_rejects_unloaded_service(
    tmp_path: Path,
) -> None:
    """Verify that ephemeris cannot be retrieved before loading."""
    settings = create_settings(tmp_path)

    service = AstronomyService(settings)

    with pytest.raises(
        RuntimeError,
        match="Ephemeris has not been loaded",
    ):
        service.get_ephemeris()