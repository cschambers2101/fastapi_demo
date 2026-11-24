import pytest


def test_get_returns_the_student(client, add_students):
    [ada] = add_students(("Ada", "Lovelace"))

    response = client.get(f"/students/{ada['id']}")

    assert response.status_code == 200
    assert response.json() == ada


def test_patch_changes_both_names(client, add_students):
    [ada] = add_students(("Ada", "Lovelace"))

    response = client.patch(
        f"/students/{ada['id']}", json={"firstname": "Augusta", "lastname": "King"}
    )

    expected = {"id": ada["id"], "firstname": "Augusta", "lastname": "King"}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.get(f"/students/{ada['id']}").json() == expected


def test_patch_ignores_id_in_body(client, add_students):
    [ada] = add_students(("Ada", "Lovelace"))

    response = client.patch(
        f"/students/{ada['id']}",
        json={"id": ada["id"] + 100, "firstname": "Augusta", "lastname": "King"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == ada["id"]
    assert client.get(f"/students/{ada['id'] + 100}").status_code == 404


def test_patch_needs_both_names(client, add_students):
    [ada] = add_students(("Ada", "Lovelace"))

    response = client.patch(f"/students/{ada['id']}", json={"firstname": "Augusta"})

    assert response.status_code == 422


def test_delete_removes_the_student(client, add_students):
    ada, alan = add_students(("Ada", "Lovelace"), ("Alan", "Turing"))

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
def test_unknown_id_returns_404(client, add_students, method, student_id):
    add_students(("Ada", "Lovelace"))

    response = call(client, method, student_id)

    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_deleting_twice_returns_404_the_second_time(client, add_students):
    [ada] = add_students(("Ada", "Lovelace"))
    client.delete(f"/students/{ada['id']}")

    response = client.delete(f"/students/{ada['id']}")

    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_patch_on_unknown_id_leaves_other_students_unchanged(client, add_students):
    [ada] = add_students(("Ada", "Lovelace"))

    client.patch("/students/999", json={"firstname": "Alan", "lastname": "Turing"})

    assert client.get("/students").json() == [ada]


@pytest.mark.parametrize("body", [{"firstname": "Ada"}, None], ids=["invalid", "none"])
def test_patch_without_valid_body_on_unknown_id_returns_422(client, body):
    response = client.patch("/students/999", json=body)

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_non_integer_id_returns_422(client, method):
    response = call(client, method, "abc")

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
@pytest.mark.parametrize("student_id", [2**63, -(2**63) - 1])
def test_id_too_large_to_store_returns_404(client, method, student_id):
    response = call(client, method, student_id)

    assert response.status_code == 404
    assert response.json() == NOT_FOUND
