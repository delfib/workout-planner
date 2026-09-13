def test_create_exercise(client, auth_headers):
    response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json["name"] == "Bench Press"
    assert response.json["category"] == "Chest"
    assert "id" in response.json


def test_create_exercise_requires_authentication(client):
    response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    })

    assert response.status_code == 401


def test_create_exercise_missing_fields(client, auth_headers):
    response = client.post("/api/exercises", json={
        "name": "Bench Press"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_create_exercise_invalid_category(client, auth_headers):
    response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Invalid Category"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Invalid category"}


def test_create_duplicate_exercise(client, auth_headers, registered_user):
    client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Exercise already exists"}


def test_create_duplicate_exercise_case_insensitive(client, auth_headers):
    client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    response = client.post("/api/exercises", json={
        "name": "bench press",
        "category": "Chest"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Exercise already exists"}


def test_get_exercises(client, auth_headers):
    client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    client.post("/api/exercises", json={
        "name": "Squat",
        "category": "Legs"
    }, headers=auth_headers)

    response = client.get("/api/exercises", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Bench Press"
    assert response.json[1]["name"] == "Squat"


def test_get_exercises_requires_authentication(client):
    response = client.get("/api/exercises")

    assert response.status_code == 401


def test_get_exercises_filters_by_category(client, auth_headers):
    client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    client.post("/api/exercises", json={
        "name": "Squat",
        "category": "Legs"
    }, headers=auth_headers)

    response = client.get(
        "/api/exercises?category=Chest",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Bench Press"


def test_get_exercises_invalid_category(client, auth_headers):
    response = client.get(
        "/api/exercises?category=Invalid",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Invalid category"}


def test_get_exercises_search(client, auth_headers):
    client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    client.post("/api/exercises", json={
        "name": "Incline Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    client.post("/api/exercises", json={
        "name": "Squat",
        "category": "Legs"
    }, headers=auth_headers)

    response = client.get(
        "/api/exercises?search=bench",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Bench Press"
    assert response.json[1]["name"] == "Incline Bench Press"


def test_update_exercise(client, auth_headers):
    create_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    exercise_id = create_response.json["id"]

    response = client.put(
        f"/api/exercises/{exercise_id}",
        json={
            "name": "Incline Bench Press",
            "category": "Chest"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["name"] == "Incline Bench Press"
    assert response.json["category"] == "Chest"


def test_update_exercise_no_fields(client, auth_headers):
    create_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    exercise_id = create_response.json["id"]

    response = client.put(
        f"/api/exercises/{exercise_id}",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "No fields to update"}


def test_update_exercise_invalid_category(client, auth_headers):
    create_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    exercise_id = create_response.json["id"]

    response = client.put(
        f"/api/exercises/{exercise_id}",
        json={"category": "Invalid"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Invalid category"}


def test_update_nonexistent_exercise(client, auth_headers):
    response = client.put(
        "/api/exercises/9999",
        json={"name": "Bench Press"},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_delete_exercise(client, auth_headers):
    create_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    exercise_id = create_response.json["id"]

    response = client.delete(
        f"/api/exercises/{exercise_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json == {
        "message": "Exercise deleted successfully"
    }

    get_response = client.get("/api/exercises", headers=auth_headers)

    assert get_response.json == []


def test_delete_nonexistent_exercise(client, auth_headers):
    response = client.delete(
        "/api/exercises/9999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_user_cannot_see_another_users_exercises(client, auth_headers, second_auth_headers):
    client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    response = client.get(
        "/api/exercises",
        headers=second_auth_headers
    )

    assert response.status_code == 200
    assert response.json == []


def test_user_cannot_update_another_users_exercise(client, auth_headers, second_auth_headers):
    create_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    exercise_id = create_response.json["id"]

    response = client.put(
        f"/api/exercises/{exercise_id}",
        json={"name": "Squat"},
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_user_cannot_delete_another_users_exercise(client, auth_headers, second_auth_headers):
    create_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    exercise_id = create_response.json["id"]

    response = client.delete(
        f"/api/exercises/{exercise_id}",
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_different_users_can_create_same_exercise(client, auth_headers, second_auth_headers):
    first_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=second_auth_headers)

    assert first_response.status_code == 201
    assert second_response.status_code == 201


def test_update_exercise_duplicate_name(client, auth_headers):
    first_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_response = client.post("/api/exercises", json={
        "name": "Squat",
        "category": "Legs"
    }, headers=auth_headers)

    exercise_id = second_response.json["id"]

    response = client.put(
        f"/api/exercises/{exercise_id}",
        json={"name": "Bench Press"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Exercise already exists"}