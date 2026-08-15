"""Application entry point for Eclipse CLI."""

from pathlib import Path

from eclipse_cli.config import load_settings
from eclipse_cli.logging import configure_logging, get_logger

logger = get_logger(__name__)
CONFIG_PATH = Path("config/settings.yaml")


def main() -> None:
    """Run the Eclipse CLI application."""
    settings = load_settings(CONFIG_PATH)

    logger.info(
        "Eclipse CLI application started in %s environment",
        settings.application.environment,
    )


if __name__ == "__main__":
    configure_logging()
    main()
