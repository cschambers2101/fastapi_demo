UNKNOWN_ID = 9999
NOT_FOUND = {"detail": "Student not found"}


def test_get_unknown_student_returns_404(client):
    response = client.get(f"/students/{UNKNOWN_ID}")
    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_patch_unknown_student_returns_404(client):
    response = client.patch(
        f"/students/{UNKNOWN_ID}",
        json={"firstname": "Ada", "lastname": "Lovelace"},
    )
    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_delete_unknown_student_returns_404(client):
    response = client.delete(f"/students/{UNKNOWN_ID}")
    assert response.status_code == 404
    assert response.json() == NOT_FOUND


def test_create_get_update_delete_happy_path(client):
    # Create
    response = client.post(
        "/students", json={"firstname": "Ada", "lastname": "Lovelace"}
    )
    assert response.status_code == 200
    created = response.json()
    student_id = created["id"]
    assert created == {"id": student_id, "firstname": "Ada", "lastname": "Lovelace"}

    # Get
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json() == created

    # Update
    response = client.patch(
        f"/students/{student_id}",
        json={"firstname": "Grace", "lastname": "Hopper"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": student_id,
        "firstname": "Grace",
        "lastname": "Hopper",
    }

    # Delete
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204

    # Gone
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 404
