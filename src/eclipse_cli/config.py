"""Application configuration models."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ApplicationSettings(BaseModel):
    """Application-level configuration."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    environment: str = Field(min_length=1)


class LoggingSettings(BaseModel):
    """Logging configuration."""

    model_config = ConfigDict(extra="forbid")

    level: str = Field(default="INFO", min_length=1)
    file: Path | None = Path("logs/eclipse-cli.log")


class Settings(BaseModel):
    """Root application configuration."""

    model_config = ConfigDict(extra="forbid")

    application: ApplicationSettings
    logging: LoggingSettings
