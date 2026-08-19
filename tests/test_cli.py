"""Tests for the command-line interface."""

import subprocess
import sys
from pathlib import Path

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


def test_cli_accepts_custom_config(
    tmp_path: Path,
) -> None:
    """Verify that the CLI accepts a custom configuration path."""
    log_file = tmp_path / "eclipse-cli.log"
    config_path = tmp_path / "settings.yaml"

    config_path.write_text(
        f"""
application:
  name: eclipse-cli
  environment: development

logging:
  level: INFO
  file: {log_file.as_posix()}
""",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["--config", str(config_path), "eclipse"],
    )

    assert result.exit_code == 0
    assert "Eclipse calculation is not implemented yet." in result.stdout


def test_cli_rejects_missing_config() -> None:
    """Verify that the CLI rejects a missing configuration file."""
    result = runner.invoke(
        app,
        [
            "--config",
            "does-not-exist.yaml",
            "eclipse",
        ],
    )

    assert result.exit_code != 0
    assert "does-not-exist.yaml" in result.output


def test_cli_accepts_short_config_option(
    tmp_path: Path,
) -> None:
    """Verify that the CLI accepts the short config option."""
    log_file = tmp_path / "eclipse-cli.log"
    config_path = tmp_path / "settings.yaml"

    config_path.write_text(
        f"""
application:
  name: eclipse-cli
  environment: development

logging:
  level: INFO
  file: {log_file.as_posix()}
""",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["-c", str(config_path), "eclipse"],
    )

    assert result.exit_code == 0
    assert "Eclipse calculation is not implemented yet." in result.stdout


def test_cli_version_ignores_config_path() -> None:
    """Verify that version output does not require configuration."""
    result = runner.invoke(
        app,
        [
            "--version",
            "--config",
            "does-not-exist.yaml",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == get_version()
