"""Tests for the application entry point."""

from pathlib import Path
import logging

import eclipse_cli.main as application
from eclipse_cli.main import main


def test_main_runs_without_error(caplog) -> None:
    """Verify that the application logs its startup message."""
    with caplog.at_level(logging.INFO):
        main()

    assert "Eclipse CLI application started" in caplog.text


def test_main_logs_application_start(caplog) -> None:
    """Verify that the application logs its startup message."""
    with caplog.at_level(logging.INFO):
        exit_code = main()

    assert exit_code == 0
    assert "Eclipse CLI application started in development environment" in (
        caplog.text
    )


def test_main_returns_configuration_error_code(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Verify that configuration errors return the expected exit code."""
    missing_config = tmp_path / "missing.yaml"

    monkeypatch.setattr(application, "CONFIG_PATH", missing_config)

    assert application.main() == 2


def test_main_returns_configuration_error_for_invalid_yaml(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Verify that invalid YAML returns the configuration error code."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text(
        "application: [invalid",
        encoding="utf-8",
    )

    monkeypatch.setattr(application, "CONFIG_PATH", config_file)

    assert application.main() == 2
