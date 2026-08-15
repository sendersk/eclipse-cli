"""Logging configuration for Eclipse CLI."""

import logging
from pathlib import Path

DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(
    level: int,
    log_file: Path | None,
) -> None:
    """
    Configure application-wide logging.

    Args:
        level: Logging level for the application.
        log_file: Optional path to the log file.
    """
    root_logger = logging.getLogger()

    # Remove existing file handlers so logging can be reconfigured safely.
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.FileHandler) or getattr(
            handler, "_eclipse_cli_handler", False
        ):
            root_logger.removeHandler(handler)
            handler.close()

    handlers: list[logging.Handler] = [
        logging.StreamHandler(),
    ]

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    for handler in handlers:
        handler.setFormatter(formatter)
        handler._eclipse_cli_handler = True  # type: ignore[attr-defined]
        root_logger.addHandler(handler)

    root_logger.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the given name.

    Args:
        name: Logger name, typically the module's ``__name__``.

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)


def parse_log_level(level: str) -> int:
    """
    Convert a textual log level into a logging constant.

    Args:
        level: Textual logging level such as ``INFO`` or ``DEBUG``.

    Returns:
        Corresponding Python logging level.

    Raises:
        ValueError: If the provided level is not supported.
    """
    normalized_level = level.upper()
    log_level = logging.getLevelNamesMapping().get(normalized_level)

    if log_level is None or not isinstance(log_level, int):
        raise ValueError(f"Unsupported logging level: {level}")

    return log_level
