import pytest


def create(client, firstname, lastname):
    return client.post(
        "/students", json={"firstname": firstname, "lastname": lastname}
    ).json()


def test_get_returns_the_student(client):
    ada = create(client, "Ada", "Lovelace")

    response = client.get(f"/students/{ada['id']}")

    assert response.status_code == 200
    assert response.json() == ada


def test_patch_changes_both_names(client):
    ada = create(client, "Ada", "Lovelace")

    response = client.patch(
        f"/students/{ada['id']}", json={"firstname": "Augusta", "lastname": "King"}
    )

    expected = {"id": ada["id"], "firstname": "Augusta", "lastname": "King"}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.get(f"/students/{ada['id']}").json() == expected


def test_patch_ignores_id_in_body(client):
    ada = create(client, "Ada", "Lovelace")

    response = client.patch(
        f"/students/{ada['id']}",
        json={"id": ada["id"] + 100, "firstname": "Augusta", "lastname": "King"},
    )

    assert response.json()["id"] == ada["id"]


def test_patch_needs_both_names(client):
    ada = create(client, "Ada", "Lovelace")

    response = client.patch(f"/students/{ada['id']}", json={"firstname": "Augusta"})

    assert response.status_code == 422


def test_delete_removes_the_student(client):
    ada = create(client, "Ada", "Lovelace")
    alan = create(client, "Alan", "Turing")

    response = client.delete(f"/students/{ada['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/students").json() == [alan]


NOT_FOUND = {"detail": "Student not found"}
UNKNOWN_IDS = [999, 0, -1]


def call(client, method, student_id):
    url = f"/students/{student_id}"
    if method == "patch":
        return client.patch(url, json={"firstname": "Ada", "lastname": "King"})
    return getattr(client, method)(url)


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
@pytest.mark.parametrize("student_id", UNKNOWN_IDS)
def test_unknown_id_returns_404(client, method, student_id):
    create(client, "Ada", "Lovelace")

    response = call(client, method, student_id)

    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_deleting_twice_returns_404_the_second_time(client):
    ada = create(client, "Ada", "Lovelace")
    client.delete(f"/students/{ada['id']}")

    response = client.delete(f"/students/{ada['id']}")

    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_patch_with_invalid_body_on_unknown_id_returns_422(client):
    response = client.patch("/students/999", json={"firstname": "Ada"})

    assert response.status_code == 422
