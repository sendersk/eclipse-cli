"""Tests for the application package structure."""

from eclipse_cli import astronomy, models, services, utils


def test_application_packages_can_be_imported() -> None:
    """Verify that all application packages can be imported."""
    assert astronomy.__name__ == "eclipse_cli.astronomy"
    assert models.__name__ == "eclipse_cli.models"
    assert services.__name__ == "eclipse_cli.services"
    assert utils.__name__ == "eclipse_cli.utils"
