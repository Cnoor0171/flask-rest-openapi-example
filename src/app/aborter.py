"""Custom exception handler utility and configuration"""
from __future__ import annotations

from http import HTTPStatus
from typing import Any, NoReturn, Type

import structlog
from flask import Flask, Response, make_response
from marshmallow_dataclass import class_schema as schema
from werkzeug.exceptions import HTTPException, default_exceptions

from .models.error import ErrorResponse

LOGGER = structlog.stdlib.get_logger()

_custom_exception_classes: dict[HTTPStatus, Type[AborterException]] = {}
ERROR_SCHEMA = schema(ErrorResponse)


class AborterException(HTTPException):
    """Custom Exception used for `abort`"""

    def __init__(self, message: str, errors: list[Any], headers: dict[str, str]):
        super().__init__()
        self.message = message
        self.errors = errors
        self.headers = headers


def abort(
    status_code: HTTPStatus,
    message: str,
    errors: list[Any] | None = None,
    headers: dict[str, str] | None = None,
) -> NoReturn:
    """Custom aborter for use in view functions. Sets status code, message and list of errors in the error response"""
    if status_code not in _custom_exception_classes:
        werk_exception = default_exceptions.get(status_code, HTTPException)

        class CustomHttpException(AborterException, werk_exception):  # type: ignore[valid-type, misc]
            """Derived class from both `AborterException` and the plethora of exception classes defined in `werkzeug`"""

        _custom_exception_classes[status_code] = CustomHttpException

    raise _custom_exception_classes[status_code](message, errors or [], headers or {})


def handle_exception(ex: Exception) -> Response:
    """
    Handles arbitrary exception from view functions.
    Return JSON with error details instead of HTML.
    Unexpected exceptions get logged and send a http.INTERNAL_SERVER_ERROR
    """
    response: Response
    data: ErrorResponse
    headers: dict[str, str] = {}
    errors: list[Any] = []

    # `data` and `data["messages"]` gets set by flask_smorest argument validators
    flask_smorest_data = getattr(ex, "data", None)
    if flask_smorest_data and "messages" in flask_smorest_data:
        errors.append(flask_smorest_data["messages"])

    if isinstance(ex, AborterException):
        response = make_response(ex.get_response())
        errors.extend(ex.errors)
        headers = ex.headers
        data = ErrorResponse(
            code=ex.code or HTTPStatus.INTERNAL_SERVER_ERROR,
            name=ex.name,
            description=ex.description or "Unkown Error",
            message=ex.message,
            errors=errors,
        )
    elif isinstance(ex, HTTPException):
        response = make_response(ex.get_response())
        data = ErrorResponse(
            code=ex.code or HTTPStatus.INTERNAL_SERVER_ERROR,
            name=ex.name,
            description=ex.description or "Unkown Error",
            message=str(ex),
            errors=errors,
        )
    else:
        LOGGER.exception("Unhandled exception")
        response = Response(status=500)
        data = ErrorResponse(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            description=HTTPStatus.INTERNAL_SERVER_ERROR.description,
            message="An unhandled exception occured in the server.",
            errors=errors,
        )

    response.data = ERROR_SCHEMA().dumps(data)
    response.content_type = "application/json"
    response.headers.update(headers)

    return response


def setup_aborter(app: Flask) -> None:
    """Sets up app custom exception handler"""
    app.register_error_handler(HTTPException, handle_exception)
    app.register_error_handler(Exception, handle_exception)
