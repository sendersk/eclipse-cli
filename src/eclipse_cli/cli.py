"""Command-line interface for Eclipse CLI."""

from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer
from typer import Context

from eclipse_cli.config import ConfigurationError, load_settings
from eclipse_cli.logging import configure_logging, get_logger, parse_log_level
from eclipse_cli.models.exceptions import InvalidLocationError
from eclipse_cli.services.eclipse import EclipseService
from eclipse_cli.services.location import LocationService

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
    version_option: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show application version and exit.",
            is_eager=True,
        ),
    ] = False,
    config_path: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
            help="Path to the YAML configuration file.",
        ),
    ] = DEFAULT_CONFIG_PATH,
) -> None:
    """Initialize the Eclipse CLI application."""
    if version_option:
        typer.echo(get_version())
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=2)

    exit_code = initialize_application(config_path)

    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command()
def eclipse(
    latitude: Annotated[
        float,
        typer.Option(
            ...,
            "--latitude",
            help="Observer latitude in decimal degrees.",
        ),
    ],
    longitude: Annotated[
        float,
        typer.Option(
            ...,
            "--longitude",
            help="Observer longitude in decimal degrees.",
        ),
    ],
) -> None:
    """Calculate the solar eclipse for a geographic location."""
    location_service = LocationService()
    eclipse_service = EclipseService()

    try:
        location = location_service.create_location(
            latitude=latitude,
            longitude=longitude,
        )
    except InvalidLocationError as error:
        typer.echo(f"Invalid location: {error}", err=True)
        raise typer.Exit(code=2) from error

    eclipse_service.calculate(location)

    typer.echo(
        f"Location: {location.latitude}, {location.longitude}",
    )
