"""Tests for the application entry point."""

import logging

from eclipse_cli.main import main


def test_main_runs_without_error(caplog) -> None:
    """Verify that the application logs its startup message."""
    with caplog.at_level(logging.INFO):
        main()

    assert "Eclipse CLI application started" in caplog.text
