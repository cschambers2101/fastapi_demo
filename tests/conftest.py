import os

import pytest

# Point the app at a test database before it is imported.
os.environ["DATABASE_URL"] = "sqlite:///./test_database.db"

from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import SQLModel  # noqa: E402

import basic_api  # noqa: E402


@pytest.fixture
def client():
    SQLModel.metadata.drop_all(basic_api.engine)
    SQLModel.metadata.create_all(basic_api.engine)
    with TestClient(basic_api.app) as test_client:
        yield test_client


@pytest.fixture
def add_students(client):
    def _add(*names):
        for firstname, lastname in names:
            response = client.post(
                "/students", json={"firstname": firstname, "lastname": lastname}
            )
            assert response.status_code == 201
    return _add
