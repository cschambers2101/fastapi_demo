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


def test_filter_ignores_case(client, add_students):
    add_students(("Will", "Smith"), ("Ada", "Lovelace"))

    lower = client.get("/students", params={"lastname": "smi"})
    upper = client.get("/students", params={"lastname": "SMI"})

    assert lastnames(lower) == ["Smith"]
    assert lastnames(upper) == ["Smith"]


def test_filter_matching_nobody_returns_empty_list(client, add_students):
    add_students(("Will", "Smith"))

    response = client.get("/students", params={"lastname": "Zed"})

    assert response.status_code == 200
    assert response.json() == []


def test_filter_ignores_case_for_accented_letters(client, add_students):
    add_students(("Mesut", "Özil"), ("Ada", "Lovelace"))

    response = client.get("/students", params={"lastname": "öz"})

    assert lastnames(response) == ["Özil"]


def test_blank_filter_returns_every_student(client, add_students):
    add_students(("Will", "Smith"), ("Ada", "Lovelace"))

    empty = client.get("/students", params={"lastname": ""})
    spaces = client.get("/students", params={"lastname": "   "})

    assert lastnames(empty) == ["Smith", "Lovelace"]
    assert lastnames(spaces) == ["Smith", "Lovelace"]


def test_filter_ignores_surrounding_spaces(client, add_students):
    add_students(("Will", "Smith"), ("Ada", "Lovelace"))

    response = client.get("/students", params={"lastname": "  Smi "})

    assert lastnames(response) == ["Smith"]


def test_percent_and_underscore_match_literally(client, add_students):
    add_students(("Will", "Smith"), ("Ada", "Lovelace"))

    percent = client.get("/students", params={"lastname": "%"})
    underscore = client.get("/students", params={"lastname": "_mith"})

    assert percent.json() == []
    assert underscore.json() == []
