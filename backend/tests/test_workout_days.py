def test_create_workout_day(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    response = client.post("/api/workout-days", json={
        "workout_id": workout_id,
        "day_of_week": "Monday"
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json["workout_id"] == workout_id
    assert response.json["day_of_week"] == "Monday"
    assert "id" in response.json


def test_create_workout_day_requires_authentication(client):
    response = client.post("/api/workout-days", json={
        "workout_id": 1,
        "day_of_week": "Monday"
    })

    assert response.status_code == 401


def test_create_workout_day_missing_fields(client, auth_headers):
    response = client.post(
        "/api/workout-days",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_create_workout_day_invalid_day(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    response = client.post("/api/workout-days", json={
        "workout_id": workout_id,
        "day_of_week": "NotADay"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {"error": "Invalid day of the week"}


def test_create_workout_day_case_insensitive(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    response = client.post("/api/workout-days", json={
        "workout_id": workout_id,
        "day_of_week": "mOnDaY"
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json["day_of_week"] == "Monday"


def test_create_workout_day_nonexistent_workout(client, auth_headers):
    response = client.post("/api/workout-days", json={
        "workout_id": 9999,
        "day_of_week": "Monday"
    }, headers=auth_headers)

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_create_duplicate_workout_day(client, auth_headers):
    first_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_workout = client.post("/api/workouts", json={
        "name": "Pull Day"
    }, headers=auth_headers)

    client.post("/api/workout-days", json={
        "workout_id": first_workout.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    response = client.post("/api/workout-days", json={
        "workout_id": second_workout.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    assert response.status_code == 400
    assert response.json == {
        "error": "A Workout is already assigned to this day"
    }

def test_get_workout_days(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    client.post("/api/workout-days", json={
        "workout_id": workout_id,
        "day_of_week": "Monday"
    }, headers=auth_headers)

    response = client.get(
        "/api/workout-days",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["day_of_week"] == "Monday"
    assert response.json[0]["workout"]["id"] == workout_id
    assert response.json[0]["workout"]["name"] == "Push Day"


def test_get_workout_days_requires_authentication(client):
    response = client.get("/api/workout-days")

    assert response.status_code == 401


def test_get_workout_days_are_sorted_by_weekday(client, auth_headers):
    workout_names = ["Wednesday Workout", "Monday Workout", "Friday Workout"]

    workout_ids = []

    for name in workout_names:
        response = client.post(
            "/api/workouts",
            json={"name": name},
            headers=auth_headers
        )
        workout_ids.append(response.json["id"])

    client.post("/api/workout-days", json={
        "workout_id": workout_ids[0],
        "day_of_week": "Wednesday"
    }, headers=auth_headers)

    client.post("/api/workout-days", json={
        "workout_id": workout_ids[1],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    client.post("/api/workout-days", json={
        "workout_id": workout_ids[2],
        "day_of_week": "Friday"
    }, headers=auth_headers)

    response = client.get(
        "/api/workout-days",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert [day["day_of_week"] for day in response.json] == [
        "Monday",
        "Wednesday",
        "Friday"
    ]


def test_update_workout_day(client, auth_headers):
    first_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_workout = client.post("/api/workouts", json={
        "name": "Pull Day"
    }, headers=auth_headers)

    create_response = client.post("/api/workout-days", json={
        "workout_id": first_workout.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    workout_day_id = create_response.json["id"]

    response = client.put(
        f"/api/workout-days/{workout_day_id}",
        json={
            "workout_id": second_workout.json["id"],
            "day_of_week": "Tuesday"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["id"] == workout_day_id
    assert response.json["workout_id"] == second_workout.json["id"]
    assert response.json["day_of_week"] == "Tuesday"


def test_update_workout_day_requires_authentication(client):
    response = client.put(
        "/api/workout-days/1",
        json={
            "workout_id": 1,
            "day_of_week": "Monday"
        }
    )

    assert response.status_code == 401


def test_update_workout_day_missing_fields(client, auth_headers):
    response = client.put(
        "/api/workout-days/1",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_update_nonexistent_workout_day(client, auth_headers):
    response = client.put(
        "/api/workout-days/9999",
        json={
            "workout_id": 1,
            "day_of_week": "Monday"
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout day not found"}


def test_update_workout_day_with_nonexistent_workout(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    create_response = client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    workout_day_id = create_response.json["id"]

    response = client.put(
        f"/api/workout-days/{workout_day_id}",
        json={
            "workout_id": 9999,
            "day_of_week": "Tuesday"
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_update_workout_day_invalid_day(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    create_response = client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    workout_day_id = create_response.json["id"]

    response = client.put(
        f"/api/workout-days/{workout_day_id}",
        json={
            "workout_id": workout_response.json["id"],
            "day_of_week": "NotADay"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Invalid day of the week"}


def test_update_workout_day_duplicate_day(client, auth_headers):
    first_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_workout = client.post("/api/workouts", json={
        "name": "Pull Day"
    }, headers=auth_headers)

    client.post("/api/workout-days", json={
        "workout_id": first_workout.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    second_day = client.post("/api/workout-days", json={
        "workout_id": second_workout.json["id"],
        "day_of_week": "Tuesday"
    }, headers=auth_headers)

    response = client.put(
        f"/api/workout-days/{second_day.json['id']}",
        json={
            "workout_id": second_workout.json["id"],
            "day_of_week": "Monday"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "A workout is already assigned to this day"
    }


def test_update_workout_day_case_insensitive(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    create_response = client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    workout_day_id = create_response.json["id"]

    response = client.put(
        f"/api/workout-days/{workout_day_id}",
        json={
            "workout_id": workout_response.json["id"],
            "day_of_week": "tUeSdAy"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["day_of_week"] == "Tuesday"


def test_delete_workout_day(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    create_response = client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    workout_day_id = create_response.json["id"]

    response = client.delete(
        f"/api/workout-days/{workout_day_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json == {
        "message": "Workout day deleted successfully"
    }

    get_response = client.get(
        "/api/workout-days",
        headers=auth_headers
    )

    assert get_response.json == []


def test_delete_workout_day_requires_authentication(client):
    response = client.delete("/api/workout-days/1")

    assert response.status_code == 401


def test_delete_nonexistent_workout_day(client, auth_headers):
    response = client.delete(
        "/api/workout-days/9999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout day not found"}


def test_user_cannot_see_another_users_workout_days(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    response = client.get(
        "/api/workout-days",
        headers=second_auth_headers
    )

    assert response.status_code == 200
    assert response.json == []


def test_user_cannot_update_another_users_workout_day(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_day_response = client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    response = client.put(
        f"/api/workout-days/{workout_day_response.json['id']}",
        json={
            "workout_id": workout_response.json["id"],
            "day_of_week": "Tuesday"
        },
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout day not found"}


def test_user_cannot_delete_another_users_workout_day(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    workout_day_response = client.post("/api/workout-days", json={
        "workout_id": workout_response.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    response = client.delete(
        f"/api/workout-days/{workout_day_response.json['id']}",
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout day not found"}


def test_different_users_can_use_same_day(client, auth_headers, second_auth_headers):
    first_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=second_auth_headers)

    first_response = client.post("/api/workout-days", json={
        "workout_id": first_workout.json["id"],
        "day_of_week": "Monday"
    }, headers=auth_headers)

    second_response = client.post("/api/workout-days", json={
        "workout_id": second_workout.json["id"],
        "day_of_week": "Monday"
    }, headers=second_auth_headers)

    assert first_response.status_code == 201
    assert second_response.status_code == 201