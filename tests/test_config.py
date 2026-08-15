"""Tests for application configuration models."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from eclipse_cli.config import Settings


def test_settings_accept_valid_configuration() -> None:
    """Verify that valid configuration data is accepted."""
    settings = Settings(
        application={
            "name": "eclipse-cli",
            "environment": "development",
        },
        logging={
            "level": "INFO",
            "file": "logs/eclipse-cli.log",
        },
    )

    assert settings.application.name == "eclipse-cli"
    assert settings.application.environment == "development"
    assert settings.logging.level == "INFO"
    assert settings.logging.file == Path("logs/eclipse-cli.log")


def test_settings_reject_unknown_fields() -> None:
    """Verify that unknown configuration fields are rejected."""
    with pytest.raises(ValidationError):
        Settings(
            application={
                "name": "eclipse-cli",
                "environment": "development",
                "unknown": "value",
            },
            logging={
                "level": "INFO",
            },
        )


def test_logging_file_can_be_disabled() -> None:
    """Verify that file logging can be disabled."""
    settings = Settings(
        application={
            "name": "eclipse-cli",
            "environment": "development",
        },
        logging={
            "level": "INFO",
            "file": None,
        },
    )

    assert settings.logging.file is None
