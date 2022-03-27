"""Resource request handlers for site instances"""

from http import HTTPStatus

import structlog
from flask.views import MethodView
from marshmallow_dataclass import class_schema as schema

from app.aborter import abort
from app.business.sites_info import get_site_by_id
from app.models.sites import GetSiteQuery, GetSiteResponse, Site

from .bp import bp

LOGGER = structlog.stdlib.get_logger()


@bp.route("/<site_id>")
class SiteView(MethodView):
    """Supported site"""

    @bp.arguments(schema(GetSiteQuery), location="query")
    @bp.response(HTTPStatus.OK, schema(GetSiteResponse))
    def get(self, qparams: GetSiteQuery, site_id: str) -> GetSiteResponse:
        """Get site details for <site_id>"""

        if qparams.throw:
            raise RuntimeError("Simulating unexpected exception on request")

        site = get_site_by_id(site_id)
        if not site:
            LOGGER.info(f"req for non existing site {site_id}")
            abort(HTTPStatus.NOT_FOUND, f"Site with id {site_id} does not exist")

        return GetSiteResponse(
            content=Site(
                id=site.id,
                name=site.name,
            )
        )
