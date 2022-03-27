"""Blueprint for actions endpoints"""
from app.api import Blueprint

bp = Blueprint(
    "Actions", __name__, description="Actions you can perform", url_prefix="/actions"
)

__all__ = [
    "bp",
]
