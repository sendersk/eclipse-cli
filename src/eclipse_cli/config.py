"""Application configuration models."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ApplicationSettings(BaseModel):
    """Application-level configuration."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    environment: str = Field(min_length=1)


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingSettings(BaseModel):
    """Logging configuration."""

    model_config = ConfigDict(extra="forbid")

    level: LogLevel = "INFO"
    file: Path | None = Path("logs/eclipse-cli.log")


class AstronomySettings(BaseModel):
    """Configuration for astronomical calculations."""

    model_config = ConfigDict(extra="forbid")

    data_directory: Path
    ephemeris: str = Field(min_length=1)


class Settings(BaseModel):
    """Root application configuration."""

    model_config = ConfigDict(extra="forbid")

    application: ApplicationSettings
    logging: LoggingSettings
    astronomy: AstronomySettings


class ConfigurationError(Exception):
    """Raised when application configuration cannot be loaded."""


def load_settings(path: Path) -> Settings:
    """
    Load and validate application settings from a YAML file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        Validated application settings.

    Raises:
        ConfigurationError: If the configuration file cannot be read or parsed.
    """
    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except OSError as error:
        raise ConfigurationError(
            f"Unable to read configuration file: {path}"
        ) from error
    except yaml.YAMLError as error:
        raise ConfigurationError(
            f"Unable to parse configuration file: {path}"
        ) from error

    try:
        return Settings.model_validate(data)
    except ValidationError as error:
        raise ConfigurationError(f"Invalid configuration data in: {path}") from error
