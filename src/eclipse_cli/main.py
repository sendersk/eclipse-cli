"""Application entry point for Eclipse CLI."""

from eclipse_cli.logging import configure_logging, get_logger

logger = get_logger(__name__)


def main() -> None:
    """Run the Eclipse CLI application."""
    logger.info("Eclipse CLI application started")


if __name__ == "__main__":
    configure_logging()
    main()
