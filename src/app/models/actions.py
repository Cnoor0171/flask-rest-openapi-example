"""Models for actions endpoints"""

from dataclasses import dataclass


@dataclass
class Action:
    """Single action"""

    id: str
    name: str


@dataclass
class GetActionResponse:
    """Response for GET instance requests"""

    content: Action


@dataclass
class GetActionQuery:
    """Accepted Query params for GET instance requests"""


@dataclass
class GetActionsResponse:
    """Response for GET collection requests"""

    content: list[Action]


@dataclass
class GetActionsQuery:
    """Accepted Query params for GET collection requests"""
