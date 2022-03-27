"""Blueprint for site posts endpoints"""
from app.api import Blueprint

bp = Blueprint(
    "Site Posts",
    __name__,
    description="Posts for a given site",
    url_prefix="/sites/<site_id>/posts",
)

__all__ = [
    "bp",
]
