"""App api configuration"""
from http import HTTPStatus
from typing import Any

from flask_smorest import Api as SmorestApi
from flask_smorest.blueprint import Blueprint as SmorestBlueprint
from marshmallow_dataclass import class_schema as schema

from app.models.error import ErrorResponse


class Api(SmorestApi):
    """`flask_smorest.Api` subclass with custom error schema"""

    ERROR_SCHEMA = schema(ErrorResponse)


class Blueprint(SmorestBlueprint):
    """`flask_smorest.blueprint.Blueprint` subclass that uses `BAD_REQUEST` on validation failures"""

    def arguments(self, *args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
        return super().arguments(
            error_status_code=HTTPStatus.BAD_REQUEST, *args, **kwargs
        )
