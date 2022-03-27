from http import HTTPStatus

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize("url", ["/api/v1/unknown", "/unknown", "/sites"])
def test_unkown_url(url: str, client: FlaskClient):
    response = client.get(url)
    api_resp = response.get_json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert api_resp["code"] == HTTPStatus.NOT_FOUND
    assert "description" in api_resp
    assert "message" in api_resp
    assert api_resp["errors"] == []


def test_unhandled_exception(client: FlaskClient):
    response = client.get("/api/v1/sites/site-1", query_string={"throw": True})
    api_resp = response.get_json()

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert api_resp["code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "description" in api_resp
    assert "unhandled exception" in api_resp["message"]
    assert api_resp["errors"] == []
