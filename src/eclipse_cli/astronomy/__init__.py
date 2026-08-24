"""Astronomy package."""

from eclipse_cli.astronomy.exceptions import EphemerisError
from eclipse_cli.astronomy.models import EphemerisData

__all__ = ["EphemerisData", "EphemerisError"]
