"""Tests for application configuration models."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from eclipse_cli.config import (
    AstronomySettings,
    ConfigurationError,
    Settings,
    load_settings,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"


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
        astronomy={
            "data_directory": "data/ephemeris",
            "ephemeris": "de440.bsp",
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
            astronomy={
                "data_directory": "data/ephemeris",
                "ephemeris": "de440.bsp",
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
        astronomy={
            "data_directory": "data/ephemeris",
            "ephemeris": "de440.bsp",
        },
    )

    assert settings.logging.file is None


def test_load_settings_from_yaml_file(tmp_path: Path) -> None:
    """Verify that settings can be loaded from a YAML file."""
    config_file = tmp_path / "settings.yaml"
    config_file.write_text(
        """
application:
    name: eclipse-cli
    environment: test
        
logging:
    level: DEBUG
    file: logs/test.log     
    
astronomy:
    data_directory: data/ephemeris
    ephemeris: de440.bsp   
""",
        encoding="utf-8",
    )

    settings = load_settings(config_file)

    assert settings.application.name == "eclipse-cli"
    assert settings.application.environment == "test"
    assert settings.logging.level == "DEBUG"
    assert settings.logging.file == Path("logs/test.log")


def test_load_settings_raises_error_for_missing_file(tmp_path: Path) -> None:
    """Verify that a missing configuration file raises an error."""
    config_file = tmp_path / "missing.yaml"

    with pytest.raises(ConfigurationError, match="Unable to read"):
        load_settings(config_file)


def test_load_settings_raises_error_for_invalid_yaml(tmp_path: Path) -> None:
    """Verify that invalid YAML raises a configuration error."""
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text(
        "application: [invalid",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="Unable to parse"):
        load_settings(config_file)


def test_default_configuration_is_valid() -> None:
    """Verify that the default project configuration is valid."""
    settings = load_settings(CONFIG_PATH)

    assert settings.application.name == "eclipse-cli"
    assert settings.application.environment == "development"
    assert settings.logging.level == "INFO"


def test_settings_reject_invalid_log_level() -> None:
    """Verify that unsupported log levels are rejected."""
    with pytest.raises(ValidationError):
        Settings(
            application={
                "name": "eclipse-cli",
                "environment": "development",
            },
            logging={
                "level": "INVALID",
            },
            astronomy={
                "data_directory": "data/ephemeris",
                "ephemeris": "de440.bsp",
            },
        )


@pytest.mark.parametrize(
    "level",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
def test_settings_accept_supported_log_levels(level: str) -> None:
    """Verify that all supported log levels are accepted."""
    settings = Settings(
        application={
            "name": "eclipse-cli",
            "environment": "development",
        },
        logging={
            "level": level,
        },
        astronomy={
            "data_directory": "data/ephemeris",
            "ephemeris": "de440.bsp",
        },
    )

    assert settings.logging.level == level


def test_logging_settings_use_defaults() -> None:
    """Verify that logging settings provide expected defaults."""
    settings = Settings(
        application={
            "name": "eclipse-cli",
            "environment": "test",
        },
        logging={},
        astronomy={
            "data_directory": "data/ephemeris",
            "ephemeris": "de440.bsp",
        },
    )

    assert settings.logging.level == "INFO"
    assert settings.logging.file == Path("logs/eclipse-cli.log")


def test_settings_reject_missing_application() -> None:
    """Verify that application settings are required."""
    with pytest.raises(ValidationError):
        Settings(
            logging={
                "level": "INFO",
            },
        )


def test_settings_reject_missing_logging() -> None:
    """Verify that logging settings are required."""
    with pytest.raises(ValidationError):
        Settings(
            application={
                "name": "eclipse-cli",
                "environment": "test",
            },
        )


def test_settings_reject_unknown_root_fields() -> None:
    """Verify that unknown root configuration fields are rejected."""
    with pytest.raises(ValidationError):
        Settings(
            application={
                "name": "eclipse-cli",
                "environment": "test",
            },
            logging={
                "level": "INFO",
            },
            unknown="value",
            astronomy={
                "data_directory": "data/ephemeris",
                "ephemeris": "de440.bsp",
            },
        )


def test_load_settings_includes_astronomy_configuration() -> None:
    """Verify that astronomy configuration is loaded correctly."""
    settings = load_settings(Path("config/settings.yaml"))

    assert settings.astronomy.data_directory == Path("data/ephemeris")
    assert settings.astronomy.ephemeris == "de440.bsp"


def test_load_settings_rejects_missing_astronomy_configuration(
    tmp_path: Path,
) -> None:
    """Verify that missing astronomy configuration is rejected."""
    config_file = tmp_path / "settings.yaml"

    config_file.write_text(
        """
application:
  name: eclipse-cli
  environment: development

logging:
  level: INFO
  file: logs/eclipse-cli.log
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError):
        load_settings(config_file)


def test_astronomy_data_directory_is_path() -> None:
    """Verify that the astronomy data directory uses pathlib."""
    settings = load_settings(Path("config/settings.yaml"))

    assert isinstance(settings.astronomy.data_directory, Path)


def test_astronomy_settings_accept_valid_configuration() -> None:
    """Verify that valid astronomy configuration is accepted."""
    settings = AstronomySettings(
        data_directory=Path("data/ephemeris"),
        ephemeris="de440.bsp",
    )

    assert settings.data_directory == Path("data/ephemeris")
    assert settings.ephemeris == "de440.bsp"
