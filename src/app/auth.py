"""
Authectication setup code.
Currently uses Basic auth with for one sample user, but can be replaced by any authetication mechanism
"""
from http import HTTPStatus

from flask import Flask, request
from werkzeug.security import check_password_hash, generate_password_hash

from .aborter import abort
from .api import Api

USERS_TO_PW_HASH = {
    # Sample user password
    "sample_user": generate_password_hash("abcdefg"),
}

UNAUTHENTICATED_ROUTES = {
    "/healthcheck",
}


def autheticate_user() -> None:
    """
    Check for Basic Auth on request
    Abort with HTTPStatus.UNAUTHORIZED if unauthorized
    """
    if request.path in UNAUTHENTICATED_ROUTES:
        return None

    auth = request.authorization
    if (
        auth
        and auth["username"]
        and auth["password"]
        and check_password_hash(
            USERS_TO_PW_HASH.get(auth["username"], ""), auth["password"]
        )
    ):
        return None

    auth_errors = []
    headers = {
        "WWW-Authenticate": 'Basic realm="Login Required"',
    }
    if not auth:
        auth_errors.append("No authorization header")
    if auth and not auth["username"]:
        auth_errors.append("No username in authorization header")
    if auth and not auth["password"]:
        auth_errors.append("No password in authorization header")
    if auth and auth["username"] and auth["username"] not in USERS_TO_PW_HASH:
        auth_errors.append("Unkown user in authorization header")
    if (
        auth
        and auth["username"]
        and auth["password"]
        and not check_password_hash(
            USERS_TO_PW_HASH.get(auth["username"], ""), auth["password"]
        )
    ):
        auth_errors.append("Incorrect password in authorization header")

    abort(
        HTTPStatus.UNAUTHORIZED,
        "Unauthorized",
        errors=[{"auth": auth_errors}],
        headers=headers,
    )


def setup_auth(app: Flask, api: Api) -> None:
    """
    Sets up authentication on the entire app and added auth docs to api schema
    """
    app.before_request(autheticate_user)

    api.spec.components.security_scheme(
        "BasicAuth", {"type": "http", "scheme": "basic"}
    )
    api.spec.options = {
        "security": [{"BasicAuth": []}],
    }
