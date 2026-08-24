"""Tests for astronomy data models."""

from pathlib import Path

import pytest
from skyfield.jpllib import SpiceKernel

from eclipse_cli.astronomy.models import EphemerisData


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
