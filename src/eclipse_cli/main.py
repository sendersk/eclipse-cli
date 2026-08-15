"""Application entry point for Eclipse CLI."""

from pathlib import Path

from eclipse_cli.config import load_settings
from eclipse_cli.logging import configure_logging, get_logger, parse_log_level

logger = get_logger(__name__)
CONFIG_PATH = Path("config/settings.yaml")


def main() -> None:
    """Run the Eclipse CLI application."""
    settings = load_settings(CONFIG_PATH)

    configure_logging(
        level=parse_log_level(settings.logging.level),
        log_file=settings.logging.file,
    )

    logger.info(
        "Eclipse CLI application started in %s environment",
        settings.application.environment,
    )


if __name__ == "__main__":
    main()
