def test_list_without_filter_returns_every_student(client, add_students):
    add_students(("Ada", "Lovelace"), ("Alan", "Turing"))

    response = client.get("/students")

    assert response.status_code == 200
    assert [s["lastname"] for s in response.json()] == ["Lovelace", "Turing"]
