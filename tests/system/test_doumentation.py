from http import HTTPStatus

import pytest
from flask.testing import FlaskClient


def test_documentation_json(client: FlaskClient):
    response = client.get("/api/v1/doc/documentation.json")
    api_resp = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert api_resp["info"]["title"]
    assert api_resp["info"]["version"] == "v1"
    assert api_resp["openapi"] == "3.0.2"

    sections = {tag["name"] for tag in api_resp["tags"]}
    assert sections == {"Sites", "Site Posts", "Actions"}

    endpoints = set(api_resp["paths"].keys())
    assert endpoints == {
        "/api/v1/sites",
        "/api/v1/sites/{site_id}",
        "/api/v1/sites/{site_id}/posts",
        "/api/v1/sites/{site_id}/posts/{post_id}",
        "/api/v1/actions",
        "/api/v1/actions/{action_id}",
    }


@pytest.mark.parametrize("ui_name", ["swagger", "redoc", "rapidoc"])
def test_ui_pages(ui_name: str, client: FlaskClient):
    response = client.get(f"/api/v1/doc/{ui_name}")

    assert response.status_code == HTTPStatus.OK
