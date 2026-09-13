def test_create_workout(client, auth_headers):
    response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json["name"] == "Push Day"
    assert "id" in response.json


def test_create_workout_requires_authentication(client):
    response = client.post("/api/workouts", json={
        "name": "Push Day"
    })

    assert response.status_code == 401


def test_create_workout_missing_name(client, auth_headers):
    response = client.post(
        "/api/workouts",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_create_workout_blank_name(client, auth_headers):
    response = client.post("/api/workouts", json={
        "name": "   "
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_create_duplicate_workout(client, auth_headers):
    client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Workout already exists"}


def test_create_duplicate_workout_case_insensitive(client, auth_headers):
    client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.post("/api/workouts", json={
        "name": "push day"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Workout already exists"}


def test_get_workouts(client, auth_headers):
    client.post("/api/workouts", json={
        "name": "Pull Day"
    }, headers=auth_headers)

    client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.get(
        "/api/workouts",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Pull Day"
    assert response.json[1]["name"] == "Push Day"


def test_get_workouts_requires_authentication(client):
    response = client.get("/api/workouts")

    assert response.status_code == 401


def test_get_workout(client, auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.get(
        f"/api/workouts/{workout_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["id"] == workout_id
    assert response.json["name"] == "Push Day"
    assert response.json["days"] == []
    assert response.json["exercises"] == []


def test_get_workout_requires_authentication(client):
    response = client.get("/api/workouts/1")

    assert response.status_code == 401


def test_get_nonexistent_workout(client, auth_headers):
    response = client.get(
        "/api/workouts/9999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_update_workout(client, auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.put(
        f"/api/workouts/{workout_id}",
        json={"name": "Upper Body"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["id"] == workout_id
    assert response.json["name"] == "Upper Body"


def test_update_workout_requires_authentication(client):
    response = client.put(
        "/api/workouts/1",
        json={"name": "Upper Body"}
    )

    assert response.status_code == 401


def test_update_workout_missing_name(client, auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.put(
        f"/api/workouts/{workout_id}",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_update_workout_blank_name(client, auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.put(
        f"/api/workouts/{workout_id}",
        json={"name": "   "},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_update_nonexistent_workout(client, auth_headers):
    response = client.put(
        "/api/workouts/9999",
        json={"name": "Upper Body"},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_update_workout_duplicate_name(client, auth_headers):
    client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_response = client.post("/api/workouts", json={
        "name": "Pull Day"
    }, headers=auth_headers)

    workout_id = second_response.json["id"]

    response = client.put(
        f"/api/workouts/{workout_id}",
        json={"name": "Push Day"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Workout already exists"}


def test_update_workout_duplicate_name_case_insensitive(client, auth_headers):
    client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_response = client.post("/api/workouts", json={
        "name": "Pull Day"
    }, headers=auth_headers)

    workout_id = second_response.json["id"]

    response = client.put(
        f"/api/workouts/{workout_id}",
        json={"name": "push day"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Workout already exists"}


def test_delete_workout(client, auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.delete(
        f"/api/workouts/{workout_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json == {
        "message": "Workout deleted successfully"
    }

    get_response = client.get(
        "/api/workouts",
        headers=auth_headers
    )

    assert get_response.json == []


def test_delete_workout_requires_authentication(client):
    response = client.delete("/api/workouts/1")

    assert response.status_code == 401


def test_delete_nonexistent_workout(client, auth_headers):
    response = client.delete(
        "/api/workouts/9999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_user_cannot_see_another_users_workout(client, auth_headers, second_auth_headers):
    client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.get(
        "/api/workouts",
        headers=second_auth_headers
    )

    assert response.status_code == 200
    assert response.json == []


def test_user_cannot_get_another_users_workout(client, auth_headers, second_auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.get(
        f"/api/workouts/{workout_id}",
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_user_cannot_update_another_users_workout(client, auth_headers, second_auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.put(
        f"/api/workouts/{workout_id}",
        json={"name": "Pull Day"},
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_user_cannot_delete_another_users_workout(client, auth_headers, second_auth_headers):
    create_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = create_response.json["id"]

    response = client.delete(
        f"/api/workouts/{workout_id}",
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_different_users_can_create_same_workout(client, auth_headers, second_auth_headers):
    first_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=second_auth_headers)

    assert first_response.status_code == 201
    assert second_response.status_code == 201