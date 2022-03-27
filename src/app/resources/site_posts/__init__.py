"""Actions endpoints"""
from .bp import bp
from .collection import SitePostsView
from .instance import SitePostView

__all__ = [
    "bp",
    "SitePostsView",
    "SitePostView",
]
