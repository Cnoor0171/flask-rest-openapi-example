"""Resource request handlers for actions instances"""
from http import HTTPStatus

from flask.views import MethodView
from marshmallow_dataclass import class_schema as schema

from app.models.site_posts import GetSitePostQuery, GetSitePostResponse, SitePost

from .bp import bp


@bp.route("/<post_id>")
class SitePostView(MethodView):
    """Post on site"""

    @bp.arguments(schema(GetSitePostQuery), location="query")
    @bp.response(HTTPStatus.OK, schema(GetSitePostResponse))
    def get(
        self, _qparams: GetSitePostQuery, site_id: str, post_id: str
    ) -> GetSitePostResponse:
        """Get post details for <post_id> on site"""
        return GetSitePostResponse(
            content=SitePost(
                id=post_id,
                site_id=site_id,
                name="",
            ),
        )
