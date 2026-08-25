"""Tests for astronomical services."""

from pathlib import Path

import pytest

from eclipse_cli.astronomy.exceptions import EphemerisError
from eclipse_cli.config import AstronomySettings
from eclipse_cli.services.astronomy import AstronomyService


def test_load_ephemeris_raises_ephemeris_error_for_missing_file(
    tmp_path: Path,
) -> None:
    """Verify that a missing ephemeris raises EphemerisError."""
    settings = AstronomySettings(
        data_directory=tmp_path,
        ephemeris="missing.bsp",
    )

    service = AstronomyService(settings)

    with pytest.raises(EphemerisError, match="missing.bsp"):
        service.load_ephemeris()