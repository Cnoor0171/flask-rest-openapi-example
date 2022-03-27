from typing import Generator

import pytest
from flask.testing import FlaskClient

from app import create_application


class AuthenticatedFlaskClient(FlaskClient):
    def open(self, *args, **kwargs):
        user = "sample_user"
        passwd = "abcdefg"
        return super().open(*args, **kwargs, auth=(user, passwd))


@pytest.fixture(scope="session")
def client() -> Generator[FlaskClient, None, None]:
    app = create_application()
    app.test_client_class = AuthenticatedFlaskClient
    yield app.test_client()


@pytest.fixture(scope="session")
def unauthed_client() -> Generator[FlaskClient, None, None]:
    app = create_application()
    yield app.test_client()
