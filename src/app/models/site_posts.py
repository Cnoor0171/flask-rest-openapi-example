"""Models for site posts endpoints"""
from dataclasses import dataclass


@dataclass
class SitePost:
    """Single site post"""

    id: str
    site_id: str
    name: str


@dataclass
class GetSitePostResponse:
    """Response for GET instance requests"""

    content: SitePost


@dataclass
class GetSitePostQuery:
    """Accepted Query params for GET instance requests"""


@dataclass
class GetSitePostsResponse:
    """Response for GET collection requests"""

    content: list[SitePost]


@dataclass
class GetSitePostsQuery:
    """Accepted Query params for GET collection requests"""
