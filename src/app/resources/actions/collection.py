"""Resource request handlers for actions collection"""
from http import HTTPStatus

from flask.views import MethodView
from marshmallow_dataclass import class_schema as schema

from app.business import actions_info
from app.models.actions import Action, GetActionsQuery, GetActionsResponse

from .bp import bp


@bp.route("")
class ActionsView(MethodView):
    """All supported actions"""

    @bp.arguments(schema(GetActionsQuery), location="query")
    @bp.response(HTTPStatus.OK, schema(GetActionsResponse))
    def get(self, _args: GetActionsQuery) -> GetActionsResponse:
        """List of all supported actions"""
        all_actions = actions_info.get_all_actions()
        return GetActionsResponse(
            content=[
                Action(
                    id=action.id,
                    name=action.name,
                )
                for action in all_actions
            ]
        )
