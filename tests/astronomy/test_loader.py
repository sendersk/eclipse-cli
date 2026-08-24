"""Tests for the ephemeris loader."""

from pathlib import Path

import pytest
from skyfield.jpllib import SpiceKernel

from eclipse_cli.astronomy import EphemerisError
from eclipse_cli.astronomy.loader import EphemerisLoader


def test_loader_rejects_missing_file(tmp_path: Path) -> None:
    """Verify that a missing ephemeris file raises an error."""
    path = tmp_path / "missing.bsp"

    loader = EphemerisLoader()

    with pytest.raises(EphemerisError, match="does not exist"):
        loader.load(path)


def test_loader_rejects_directory(tmp_path: Path) -> None:
    """Verify that a directory cannot be used as an ephemeris file."""
    path = tmp_path / "ephemeris"
    path.mkdir()

    loader = EphemerisLoader()

    with pytest.raises(EphemerisError, match="is not a file"):
        loader.load(path)


def test_loader_returns_ephemeris_data(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that a valid ephemeris is returned as application data."""
    path = tmp_path / "de440.bsp"
    path.touch()

    kernel = SpiceKernel.__new__(SpiceKernel)

    def fake_load_file(load_path: Path) -> SpiceKernel:
        """Return a fake kernel for testing."""
        assert load_path == path
        return kernel

    monkeypatch.setattr(
        "eclipse_cli.astronomy.loader.load_file",
        fake_load_file,
    )

    loader = EphemerisLoader()

    result = loader.load(path)

    assert result.path == path
    assert result.kernel is kernel


def test_loader_wraps_loading_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that loading errors are wrapped in EphemerisError."""
    path = tmp_path / "de440.bsp"
    path.touch()

    def fake_load_file(path: Path) -> SpiceKernel:
        """Raise an error simulating a failed ephemeris load."""
        raise RuntimeError("Unable to parse kernel")

    monkeypatch.setattr(
        "eclipse_cli.astronomy.loader.load_file",
        fake_load_file,
    )

    loader = EphemerisLoader()

    with pytest.raises(EphemerisError, match="Unable to load ephemeris file"):
        loader.load(path)


def test_loader_preserves_original_loading_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that the original loading error is preserved as the cause."""
    path = tmp_path / "de440.bsp"
    path.touch()

    original_error = RuntimeError("Unable to parse kernel")

    def fake_load_file(path: Path) -> SpiceKernel:
        """Raise the original loading error."""
        raise original_error

    monkeypatch.setattr(
        "eclipse_cli.astronomy.loader.load_file",
        fake_load_file,
    )

    loader = EphemerisLoader()

    with pytest.raises(EphemerisError) as exc_info:
        loader.load(path)

    assert exc_info.value.__cause__ is original_error
