"""Resource request handlers for site posts collection"""
from http import HTTPStatus

from flask.views import MethodView
from marshmallow_dataclass import class_schema as schema

from app.models.site_posts import GetSitePostsQuery, GetSitePostsResponse

from .bp import bp


@bp.route("")
class SitePostsView(MethodView):
    """All posts on site"""

    @bp.arguments(schema(GetSitePostsQuery), location="query")
    @bp.response(HTTPStatus.OK, schema(GetSitePostsResponse))
    def get(self, _args: GetSitePostsQuery) -> GetSitePostsResponse:
        """List of all posts on site"""
        return GetSitePostsResponse(content=[])
