"""Tests for the command-line interface."""

import subprocess
import sys

from typer.testing import CliRunner

from eclipse_cli.cli import app, get_version

runner = CliRunner()


def test_get_version_returns_package_version() -> None:
    """Verify that the application version is available."""
    version = get_version()

    assert version


def test_cli_help() -> None:
    """Verify that the CLI exposes help information."""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Calculate and display solar eclipse information" in result.stdout


def test_cli_version() -> None:
    """Verify that the CLI exposes the application version."""
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == get_version()


def test_eclipse_command() -> None:
    """Verify that the eclipse command is available."""
    result = runner.invoke(app, ["eclipse"])

    assert result.exit_code == 0
    assert "Eclipse calculation is not implemented yet." in result.stdout


def test_cli_version_as_process() -> None:
    """Verify that the CLI process returns the application version."""
    result = subprocess.run(
        [sys.executable, "-m", "eclipse_cli.main", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == get_version()


def test_cli_version_does_not_initialize_application(
    monkeypatch,
) -> None:
    """Verify that the version option bypasses application initialization."""

    def fail_initialization() -> int:
        raise AssertionError("Application initialization should not run.")

    monkeypatch.setattr(
        "eclipse_cli.cli.initialize_application",
        fail_initialization,
    )

    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == get_version()


def test_cli_without_command_shows_help() -> None:
    """Verify that the CLI shows help when no command is provided."""
    result = runner.invoke(app, [])

    assert result.exit_code == 2
    assert "Calculate and display solar eclipse information" in result.stdout
