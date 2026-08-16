"""Application entry point for Eclipse CLI."""

from pathlib import Path

from eclipse_cli.config import ConfigurationError, load_settings
from eclipse_cli.logging import configure_logging, get_logger, parse_log_level

logger = get_logger(__name__)
CONFIG_PATH = Path("config/settings.yaml")


def main() -> int:
    """Run the Eclipse CLI application."""
    try:
        settings = load_settings(CONFIG_PATH)

        configure_logging(
            level=parse_log_level(settings.logging.level),
            log_file=settings.logging.file,
        )
    except ConfigurationError as error:
        logger.error("Configuration error: %s", error)
        return 2

    logger.info(
        "Eclipse CLI application started in %s environment",
        settings.application.environment,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
