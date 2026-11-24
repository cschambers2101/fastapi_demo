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
