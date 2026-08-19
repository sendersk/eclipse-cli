"""Tests for the application entry point."""

import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from eclipse_cli.cli import (
    CONFIGURATION_ERROR_EXIT_CODE,
    app,
    initialize_application,
)

runner = CliRunner()


def test_initialize_application_returns_zero() -> None:
    """Verify that application initialization succeeds."""
    exit_code = initialize_application(
        Path("config/settings.yaml"),
    )

    assert exit_code == 0


def test_initialize_application_returns_configuration_error(
    tmp_path: Path,
) -> None:
    """Verify that configuration errors return the expected exit code."""
    config_path = tmp_path / "missing.yaml"

    exit_code = initialize_application(config_path)

    assert exit_code == CONFIGURATION_ERROR_EXIT_CODE


def test_initialize_application_returns_error_for_invalid_yaml(
    tmp_path: Path,
) -> None:
    """Verify that invalid YAML returns the configuration error code."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text(
        "application: [invalid",
        encoding="utf-8",
    )

    exit_code = initialize_application(config_file)

    assert exit_code == CONFIGURATION_ERROR_EXIT_CODE


def test_initialize_application_returns_error_for_invalid_settings(
    tmp_path: Path,
) -> None:
    """Verify that invalid settings return the configuration error code."""
    config_file = tmp_path / "settings.yaml"
    config_file.write_text(
        """
application:
  name: eclipse-cli
  environment: development

logging:
  level: INVALID
  file: logs/eclipse-cli.log
""",
        encoding="utf-8",
    )

    exit_code = initialize_application(config_file)

    assert exit_code == CONFIGURATION_ERROR_EXIT_CODE


def test_application_shows_help_without_command() -> None:
    """Verify that the application shows help when no command is provided."""
    result = subprocess.run(
        [sys.executable, "-m", "eclipse_cli.main"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Calculate and display solar eclipse information" in result.stdout


def test_cli_help() -> None:
    """Verify that the CLI exposes help information."""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Calculate and display solar eclipse information" in result.stdout


def test_eclipse_command() -> None:
    """Verify that the eclipse command is available."""
    result = runner.invoke(
        app,
        [
            "eclipse",
            "--latitude",
            "52.5200",
            "--longitude",
            "13.4050",
        ],
    )

    assert result.exit_code == 0
    assert "Location: 52.52, 13.405" in result.stdout
