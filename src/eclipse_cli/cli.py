"""Command-line interface for Eclipse CLI."""

from importlib.metadata import version
from pathlib import Path

import typer
from typer import Context

from eclipse_cli.config import ConfigurationError, load_settings
from eclipse_cli.logging import configure_logging, get_logger, parse_log_level

logger = get_logger(__name__)

DEFAULT_CONFIG_PATH = Path("config/settings.yaml")
CONFIGURATION_ERROR_EXIT_CODE = 2
PACKAGE_NAME = "eclipse-cli"


app = typer.Typer(
    name="eclipse-cli",
    help="Calculate and display solar eclipse information for a location.",
    invoke_without_command=True,
)


def get_version() -> str:
    """Return the installed application version."""
    return version(PACKAGE_NAME)


def initialize_application(config_path: Path) -> int:
    """Initialize application configuration and logging.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Zero on success or the configuration error exit code.
    """
    try:
        settings = load_settings(config_path)

        configure_logging(
            level=parse_log_level(settings.logging.level),
            log_file=settings.logging.file,
        )
    except ConfigurationError as error:
        logger.error("Configuration error: %s", error)
        return CONFIGURATION_ERROR_EXIT_CODE

    logger.info(
        "Eclipse CLI application started in %s environment",
        settings.application.environment,
    )

    return 0


@app.callback()
def cli_callback(
    ctx: Context,
    version_option: bool = typer.Option(
        False,
        "--version",
        help="Show application version and exit.",
        is_eager=True,
    ),
) -> None:
    """Initialize the Eclipse CLI application."""
    if version_option:
        typer.echo(get_version())
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=2)

    exit_code = initialize_application(DEFAULT_CONFIG_PATH)

    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command()
def eclipse() -> None:
    """Calculate solar eclipse information for a location."""
    typer.echo("Eclipse calculation is not implemented yet.")
