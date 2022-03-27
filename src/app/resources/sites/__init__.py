"""Sites endpoints"""
from .bp import bp
from .collection import SitesView
from .instance import SiteView

__all__ = [
    "bp",
    "SitesView",
    "SiteView",
]
