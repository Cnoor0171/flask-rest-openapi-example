from http import HTTPStatus

from flask.testing import FlaskClient

from app.version import __version__


def test_healthcheck_without_auth(unauthed_client: FlaskClient):
    response = unauthed_client.get("/healthcheck")
    api_resp = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert api_resp["version"] == __version__
