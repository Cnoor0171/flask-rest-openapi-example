"""Blueprint for sites endpoints"""
from app.api import Blueprint

bp = Blueprint(
    "Sites", __name__, description="Sites with scrapers", url_prefix="/sites"
)

__all__ = [
    "bp",
]
