def test_list_without_filter_returns_every_student(client, add_students):
    add_students(("Ada", "Lovelace"), ("Alan", "Turing"))

    response = client.get("/students")

    assert response.status_code == 200
    assert [s["lastname"] for s in response.json()] == ["Lovelace", "Turing"]


def lastnames(response):
    return [s["lastname"] for s in response.json()]


def test_filter_returns_students_whose_surname_starts_with_text(client, add_students):
    add_students(("Will", "Smith"), ("Jo", "Smithson"), ("Ada", "Lovelace"))

    response = client.get("/students", params={"lastname": "Smi"})

    assert response.status_code == 200
    assert lastnames(response) == ["Smith", "Smithson"]
