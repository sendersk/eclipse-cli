"""Logging configuration for Eclipse CLI."""

import logging
from pathlib import Path

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DEFAULT_LOG_FILE = Path("logs/eclipse-cli.log")


def configure_logging(
        level: int = DEFAULT_LOG_LEVEL,
        log_file: Path | None = DEFAULT_LOG_FILE,
) -> None:
    """
    Configure application-wide logging.

    Args:
          level: Logging level for the application.
          log_file: Optional path to the log file.
    """
    handlers: list[logging.Handler] = [
        logging.StreamHandler(),
    ]

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format=DEFAULT_LOG_FORMAT,
        handlers=handlers,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the given name.

    Args:
        name: Logger name, typically the module's ``__name__``.

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)