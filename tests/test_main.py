"""Tests for the application entry point."""

from eclipse_cli.main import main


def test_main_runs_without_error() -> None:
    """Verify that the application entry point runs successfully."""
    main()
