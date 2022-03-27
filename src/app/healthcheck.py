"""Add healthcheck endpoint"""
from flask import Flask

from .version import __version__


def healthcheck_endpoint() -> dict[str, str]:
    """Returns the package version wih HTTPStatus.OK immediately"""
    return {"version": __version__}


def setup_healthcheck(app: Flask) -> None:
    """Add healthcheck endpoint for checking app status"""
    app.add_url_rule("/healthcheck", view_func=healthcheck_endpoint)
