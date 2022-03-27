"""Actions endpoints"""
from .bp import bp
from .collection import ActionsView
from .instance import ActionView

__all__ = [
    "bp",
    "ActionsView",
    "ActionView",
]
