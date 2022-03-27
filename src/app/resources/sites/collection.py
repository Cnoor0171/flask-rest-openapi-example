"""Resource request handlers for site collection"""
import math
from http import HTTPStatus

from flask.views import MethodView
from marshmallow_dataclass import class_schema as schema

from app.business.sites_info import get_all_sites
from app.models.pagination import Pagination
from app.models.sites import GetSitesQuery, GetSitesResponse, Site

from .bp import bp


@bp.route("")
class SitesView(MethodView):
    """All supported sites"""

    @bp.arguments(schema(GetSitesQuery), location="query")
    @bp.response(HTTPStatus.OK, schema(GetSitesResponse))
    def get(self, qparams: GetSitesQuery) -> GetSitesResponse:
        """List of all supported sites"""

        sites = get_all_sites()
        total = len(sites)
        sites = sites[
            qparams.page * qparams.page_size : (qparams.page + 1) * qparams.page_size
        ]

        return GetSitesResponse(
            content=[Site(id=site.id, name=site.name) for site in sites],
            pagination=Pagination(
                current=qparams.page,
                page_size=qparams.page_size,
                next=qparams.page + 1
                if 0 <= (qparams.page + 1) * qparams.page_size < total
                else None,
                prev=qparams.page - 1
                if 0 <= (qparams.page - 1) * qparams.page_size < total
                else None,
                page_count=math.ceil(total / qparams.page_size),
            ),
        )
