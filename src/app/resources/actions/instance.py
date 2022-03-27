"""Resource request handlers for action instances"""
from http import HTTPStatus

from flask.views import MethodView
from marshmallow_dataclass import class_schema as schema

from app.aborter import abort
from app.business import actions_info
from app.models.actions import Action, GetActionQuery, GetActionResponse

from .bp import bp


@bp.route("/<action_id>")
class ActionView(MethodView):
    """Supported action"""

    @bp.arguments(schema(GetActionQuery), location="query")
    @bp.response(HTTPStatus.OK, schema(GetActionResponse))
    def get(self, _args: GetActionQuery, action_id: str) -> GetActionResponse:
        """Get site details for <action_id>"""
        action = actions_info.get_action_by_id(action_id)
        if not action:
            abort(HTTPStatus.NOT_FOUND, f"Action with id {action_id} does not exist")

        return GetActionResponse(
            content=Action(
                id=action.id,
                name=action.name,
            )
        )
