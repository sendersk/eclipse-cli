"""Exceptions raised by domain models."""


class InvalidLocationError(ValueError):
    """Raised when geographic coordinates are outside valid ranges."""


class EphemerisError(Exception):
    """Raised when an ephemeris cannot be loaded."""
