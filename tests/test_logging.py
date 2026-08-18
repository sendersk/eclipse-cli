"""Tests for application logging."""

import logging
from pathlib import Path

from eclipse_cli.cli import DEFAULT_CONFIG_PATH
from eclipse_cli.config import load_settings
from eclipse_cli.logging import configure_logging, get_logger, parse_log_level


def test_get_logger_returns_named_logger() -> None:
    """Verify that get_logger returns a logger with the requested name."""
    logger = get_logger("test.logger")

    assert logger.name == "test.logger"


def test_configure_logging_creates_log_file(tmp_path: Path) -> None:
    """Verify that logging configuration creates the requested log file."""
    log_file = tmp_path / "application.log"

    configure_logging(
        level=logging.INFO,
        log_file=log_file,
    )

    logger = get_logger("test.application")
    logger.info("test message")

    for handler in logging.getLogger().handlers:
        handler.flush()

    assert log_file.exists()
    assert "test message" in log_file.read_text(encoding="utf-8")


def test_configure_logging_without_file_uses_console_only() -> None:
    """Verify that file logging can be disabled."""
    configure_logging(
        level=logging.INFO,
        log_file=None,
    )

    root_logger = logging.getLogger()

    assert all(
        not isinstance(handler, logging.FileHandler) for handler in root_logger.handlers
    )


def test_parse_log_level_returns_logging_constant() -> None:
    """Verify that textual log levels are converted correctly."""
    assert parse_log_level("DEBUG") == logging.DEBUG
    assert parse_log_level("INFO") == logging.INFO
    assert parse_log_level("WARNING") == logging.WARNING
    assert parse_log_level("ERROR") == logging.ERROR
    assert parse_log_level("CRITICAL") == logging.CRITICAL


def test_default_configuration_uses_valid_log_level() -> None:
    """Verify that the default YAML contains a supported log level."""
    settings = load_settings(DEFAULT_CONFIG_PATH)

    assert settings.logging.level in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }
