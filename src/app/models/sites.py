"""Models for sites endpoints"""
from dataclasses import dataclass, field

from marshmallow.validate import Range

from .pagination import Pagination


@dataclass
class Site:
    """Single site"""

    id: str
    name: str


@dataclass
class GetSiteResponse:
    """Response for GET instance requests"""

    content: Site


@dataclass
class GetSitesResponse:
    """Accepted Query params for GET instance requests"""

    content: list[Site]
    pagination: Pagination


@dataclass
class GetSiteQuery:
    """Response for GET collection requests"""

    throw: bool = False


@dataclass
class GetSitesQuery:
    """Accepted Query params for GET collection requests"""

    page: int = field(default=0)
    page_size: int = field(default=20, metadata={"validate": Range(min=1, max=100)})
