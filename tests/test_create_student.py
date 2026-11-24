import pytest


@pytest.mark.parametrize(
    "body",
    [{}, {"firstname": "Ada"}, {"lastname": "Lovelace"}],
    ids=["empty", "no lastname", "no firstname"],
)
def test_create_without_both_names_returns_422(client, body):
    response = client.post("/students", json=body)

    assert response.status_code == 422
    assert client.get("/students").json() == []


def test_create_ignores_id_sent_by_client(client):
    first = client.post(
        "/students", json={"id": 7, "firstname": "Ada", "lastname": "Lovelace"}
    )
    second = client.post(
        "/students", json={"id": 7, "firstname": "Alan", "lastname": "Turing"}
    )

    assert first.json()["id"] == 1
    assert second.json()["id"] == 2
