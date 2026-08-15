"""Tests for application logging."""

import logging
from pathlib import Path

from eclipse_cli.logging import configure_logging, get_logger


def test_get_logger_returns_named_logger() -> None:
    """Verify that get_logger returns a logger with the requested name."""
    logger = get_logger("test.logger")

    assert logger.name == "test.logger"


def test_configure_logging_creates_log_file(tmp_path: Path) -> None:
    """Verify that logging configuration creates the requested log file."""
    log_file = tmp_path / "application.log"

    configure_logging(log_file=log_file)

    logger = get_logger("test.application")
    logger.info("test message")

    for handler in logging.getLogger().handlers:
        handler.flush()

    assert log_file.exists()
    assert "test message" in log_file.read_text(encoding="utf-8")


def test_configure_logging_without_file_uses_console_only() -> None:
    """Verify that file logging can be disabled."""
    configure_logging(log_file=None)

    root_logger = logging.getLogger()

    assert all(
        not isinstance(handler, logging.FileHandler)
        for handler in root_logger.handlers
    )