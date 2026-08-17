"""Command-line interface for Eclipse CLI."""

import typer

app = typer.Typer(
    name="eclipse-cli",
    help="Calculate and display solar eclipse information for a location",
    no_args_is_help=True,
)


@app.command()
def eclipse() -> None:
    """Calculate solar eclipse information for a location."""
    typer.echo("Eclipse calculation is not implemented yet.")
