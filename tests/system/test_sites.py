from http import HTTPStatus
from typing import Any

from flask.testing import FlaskClient

from tests.utils.nice_params import nice_parametrize


def test_all_sites(client: FlaskClient):
    response = client.get("/api/v1/sites")
    api_resp = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(api_resp["content"], list)
    assert api_resp["pagination"]["current"] == 0
    assert api_resp["pagination"]["page_size"] == 20
    assert api_resp["pagination"]["prev"] is None


def test_all_sites_invalid_qparam(client: FlaskClient):
    response = client.get(
        "/api/v1/sites", query_string={"page": "asd", "page_size": "wda"}
    )
    api_resp = response.get_json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert api_resp["code"] == HTTPStatus.BAD_REQUEST
    assert len(api_resp["errors"]) == 1
    assert "query" in api_resp["errors"][0]
    assert "page" in api_resp["errors"][0]["query"]
    assert "page_size" in api_resp["errors"][0]["query"]


@nice_parametrize(
    {
        "page": 0,
        "page_size": 2,
        "exp_len": 2,
        "exp_pagination": {
            "current": 0,
            "page_size": 2,
            "page_count": 2,
            "prev": None,
            "next": 1,
        },
    },
    {
        "page": 1,
        "page_size": 2,
        "exp_len": 1,
        "exp_pagination": {
            "current": 1,
            "page_size": 2,
            "page_count": 2,
            "prev": 0,
            "next": None,
        },
    },
    {
        "page": 0,
        "page_size": 3,
        "exp_len": 3,
        "exp_pagination": {
            "current": 0,
            "page_size": 3,
            "page_count": 1,
            "prev": None,
            "next": None,
        },
    },
    {
        "page": 1000,
        "page_size": 2,
        "exp_len": 0,
        "exp_pagination": {
            "current": 1000,
            "page_size": 2,
            "page_count": 2,
            "prev": None,
            "next": None,
        },
    },
    {
        "page": 1,
        "page_size": 0,
        "exp_status": HTTPStatus.BAD_REQUEST,
    },
)
def test_all_sites_pagination(
    page: int,
    page_size: int,
    exp_len: int,
    exp_status: HTTPStatus | None,
    exp_pagination: Any,
    client: FlaskClient,
):
    response = client.get(
        "/api/v1/sites", query_string={"page": page, "page_size": page_size}
    )
    api_resp = response.get_json()
    assert response.status_code == (HTTPStatus.OK if exp_status is None else exp_status)
    if exp_len is not None:
        assert len(api_resp["content"]) == exp_len
    if exp_pagination is not None:
        assert api_resp["pagination"] == exp_pagination


def test_site_by_id(client: FlaskClient):
    response = client.get("/api/v1/sites/site-1")
    api_resp = response.get_json()

    assert response.status_code == HTTPStatus.OK
    assert api_resp
    assert isinstance(api_resp["content"], dict)
    assert api_resp["content"]["id"] == "site-1"
    assert api_resp["content"]["name"] == "Site 1"


def test_site_by_invalid_id(client: FlaskClient):
    response = client.get("/api/v1/sites/sdflkjsdf")

    assert response.status_code == HTTPStatus.NOT_FOUND
