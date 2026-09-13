def test_add_exercise_to_workout(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets of 8 reps"
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json["workout_id"] == workout_response.json["id"]
    assert response.json["exercise_id"] == exercise_response.json["id"]
    assert response.json["description"] == "4 sets of 8 reps"
    assert response.json["position"] == 1
    assert "id" in response.json


def test_add_exercise_to_workout_requires_authentication(client):
    response = client.post(
        "/api/workouts/1/exercises",
        json={
            "exercise_id": 1,
            "description": "4 sets of 8 reps"
        }
    )

    assert response.status_code == 401


def test_add_exercise_to_workout_missing_fields(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_add_exercise_to_workout_blank_description(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "   "
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_add_exercise_to_nonexistent_workout(client, auth_headers):
    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    response = client.post(
        "/api/workouts/9999/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets of 8 reps"
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_add_nonexistent_exercise_to_workout(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": 9999,
            "description": "4 sets of 8 reps"
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_add_duplicate_exercise_to_workout(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]
    exercise_id = exercise_response.json["id"]

    client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": exercise_id,
            "description": "4 sets of 8 reps"
        },
        headers=auth_headers
    )

    response = client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": exercise_id,
            "description": "3 sets of 10 reps"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "Exercise already added to workout"
    }


def test_add_exercises_assigns_positions(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    bench_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    incline_response = client.post("/api/exercises", json={
        "name": "Incline Press",
        "category": "Chest"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    first_response = client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": bench_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    second_response = client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": incline_response.json["id"],
            "description": "3 sets"
        },
        headers=auth_headers
    )

    assert first_response.json["position"] == 1
    assert second_response.json["position"] == 2


def test_get_workout_exercises(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets of 8 reps"
        },
        headers=auth_headers
    )

    response = client.get(
        f"/api/workouts/{workout_id}/exercises",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["exercise"]["id"] == exercise_response.json["id"]
    assert response.json[0]["exercise"]["name"] == "Bench Press"
    assert response.json[0]["exercise"]["category"] == "Chest"
    assert response.json[0]["description"] == "4 sets of 8 reps"
    assert response.json[0]["position"] == 1


def test_get_workout_exercises_empty_workout(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    response = client.get(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json == []


def test_get_workout_exercises_requires_authentication(client):
    response = client.get("/api/workouts/1/exercises")

    assert response.status_code == 401


def test_get_workout_exercises_nonexistent_workout(client, auth_headers):
    response = client.get(
        "/api/workouts/9999/exercises",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_get_workout_exercises_are_sorted_by_position(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    first_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_exercise = client.post("/api/exercises", json={
        "name": "Shoulder Press",
        "category": "Shoulders"
    }, headers=auth_headers)

    third_exercise = client.post("/api/exercises", json={
        "name": "Tricep Pushdown",
        "category": "Arms"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": first_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": second_exercise.json["id"],
            "description": "3 sets"
        },
        headers=auth_headers
    )

    client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": third_exercise.json["id"],
            "description": "3 sets"
        },
        headers=auth_headers
    )

    response = client.get(
        f"/api/workouts/{workout_id}/exercises",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert [
        exercise["exercise"]["name"]
        for exercise in response.json
    ] == [
        "Bench Press",
        "Shoulder Press",
        "Tricep Pushdown"
    ]


def test_update_workout_exercise_description(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "description": "4 sets of 8 reps"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["description"] == "4 sets of 8 reps"
    assert response.json["exercise"]["name"] == "Bench Press"
    assert response.json["position"] == 1


def test_update_workout_exercise_exercise(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    first_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_exercise = client.post("/api/exercises", json={
        "name": "Incline Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": first_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "exercise_id": second_exercise.json["id"]
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["exercise"]["id"] == second_exercise.json["id"]
    assert response.json["exercise"]["name"] == "Incline Press"
    assert response.json["description"] == "4 sets"
    assert response.json["position"] == 1


def test_update_workout_exercise_multiple_fields(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    first_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_exercise = client.post("/api/exercises", json={
        "name": "Incline Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": first_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "exercise_id": second_exercise.json["id"],
            "description": "3 sets of 10 reps",
            "position": 2
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["exercise"]["id"] == second_exercise.json["id"]
    assert response.json["description"] == "3 sets of 10 reps"
    assert response.json["position"] == 2


def test_update_workout_exercise_requires_authentication(client):
    response = client.put(
        "/api/workout-exercises/1",
        json={
            "description": "Updated"
        }
    )

    assert response.status_code == 401


def test_update_workout_exercise_with_no_fields(client, auth_headers):
    response = client.put(
        "/api/workout-exercises/9999",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {"error": "No fields to update"}


def test_update_nonexistent_workout_exercise(client, auth_headers):
    response = client.put(
        "/api/workout-exercises/9999",
        json={
            "description": "Updated"
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {
        "error": "Workout exercise not found"
    }


def test_update_workout_exercise_with_nonexistent_exercise(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "exercise_id": 9999
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_update_workout_exercise_with_blank_description(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "description": "   "
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "Description cannot be empty"
    }

def test_update_workout_exercise_to_duplicate_exercise(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    first_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_exercise = client.post("/api/exercises", json={
        "name": "Incline Press",
        "category": "Chest"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    first_add = client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": first_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    second_add = client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": second_exercise.json["id"],
            "description": "3 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{second_add.json['id']}",
        json={
            "exercise_id": first_exercise.json["id"]
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "Exercise already added to workout"
    }


def test_update_workout_exercise_to_occupied_position(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    first_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_exercise = client.post("/api/exercises", json={
        "name": "Incline Press",
        "category": "Chest"
    }, headers=auth_headers)

    workout_id = workout_response.json["id"]

    client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": first_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    second_add = client.post(
        f"/api/workouts/{workout_id}/exercises",
        json={
            "exercise_id": second_exercise.json["id"],
            "description": "3 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{second_add.json['id']}",
        json={
            "position": 1
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "Position already occupied in workout"
    }


def test_get_workout_exercises_cannot_access_other_users_workout(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Private Workout"
    }, headers=auth_headers)

    response = client.get(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_add_exercise_to_other_users_workout(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Private Workout"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=second_auth_headers)

    response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}


def test_add_other_users_exercise_to_own_workout(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "My Workout"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=second_auth_headers)

    response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_update_other_users_workout_exercise(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Private Workout"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "description": "Hacked"
        },
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {
        "error": "Workout exercise not found"
    }


def test_update_workout_exercise_with_other_users_exercise(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "My Workout"
    }, headers=auth_headers)

    my_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    other_exercise = client.post("/api/exercises", json={
        "name": "Squat",
        "category": "Legs"
    }, headers=second_auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": my_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.put(
        f"/api/workout-exercises/{add_response.json['id']}",
        json={
            "exercise_id": other_exercise.json["id"]
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"error": "Exercise not found"}


def test_delete_other_users_workout_exercise(client, auth_headers, second_auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Private Workout"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.delete(
        f"/api/workout-exercises/{add_response.json['id']}",
        headers=second_auth_headers
    )

    assert response.status_code == 404
    assert response.json == {
        "error": "Workout exercise not found"
    }

def test_delete_workout_exercise(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercise_response = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    add_response = client.post(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        json={
            "exercise_id": exercise_response.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    response = client.delete(
        f"/api/workout-exercises/{add_response.json['id']}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json == {
        "message": "Workout exercise deleted successfully"
    }

    get_response = client.get(
        f"/api/workouts/{workout_response.json['id']}/exercises",
        headers=auth_headers
    )

    assert get_response.status_code == 200
    assert get_response.json == []


def test_delete_workout_exercise_requires_authentication(client):
    response = client.delete("/api/workout-exercises/1")

    assert response.status_code == 401


def test_delete_nonexistent_workout_exercise(client, auth_headers):
    response = client.delete(
        "/api/workout-exercises/9999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {
        "error": "Workout exercise not found"
    }


def test_delete_first_workout_exercise_renumbers_positions(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercises = []

    for name in ["Bench Press", "Shoulder Press", "Tricep Pushdown"]:
        response = client.post("/api/exercises", json={
            "name": name,
            "category": "Chest"
        }, headers=auth_headers)
        exercises.append(response.json["id"])

    workout_id = workout_response.json["id"]

    added = []

    for exercise_id in exercises:
        response = client.post(
            f"/api/workouts/{workout_id}/exercises",
            json={
                "exercise_id": exercise_id,
                "description": "3 sets"
            },
            headers=auth_headers
        )
        added.append(response.json["id"])

    response = client.delete(
        f"/api/workout-exercises/{added[0]}",
        headers=auth_headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/workouts/{workout_id}/exercises",
        headers=auth_headers
    )

    assert [
        exercise["exercise"]["name"]
        for exercise in get_response.json
    ] == [
        "Shoulder Press",
        "Tricep Pushdown"
    ]

    assert [
        exercise["position"]
        for exercise in get_response.json
    ] == [1, 2]


def test_delete_middle_workout_exercise_renumbers_positions(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercises = []

    for name in ["Bench Press", "Shoulder Press", "Tricep Pushdown"]:
        response = client.post("/api/exercises", json={
            "name": name,
            "category": "Chest"
        }, headers=auth_headers)
        exercises.append(response.json["id"])

    workout_id = workout_response.json["id"]

    added = []

    for exercise_id in exercises:
        response = client.post(
            f"/api/workouts/{workout_id}/exercises",
            json={
                "exercise_id": exercise_id,
                "description": "3 sets"
            },
            headers=auth_headers
        )
        added.append(response.json["id"])

    response = client.delete(
        f"/api/workout-exercises/{added[1]}",
        headers=auth_headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/workouts/{workout_id}/exercises",
        headers=auth_headers
    )

    assert [
        exercise["exercise"]["name"]
        for exercise in get_response.json
    ] == [
        "Bench Press",
        "Tricep Pushdown"
    ]

    assert [
        exercise["position"]
        for exercise in get_response.json
    ] == [1, 2]


def test_delete_last_workout_exercise_keeps_previous_positions(client, auth_headers):
    workout_response = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    exercises = []

    for name in ["Bench Press", "Shoulder Press", "Tricep Pushdown"]:
        response = client.post("/api/exercises", json={
            "name": name,
            "category": "Chest"
        }, headers=auth_headers)
        exercises.append(response.json["id"])

    workout_id = workout_response.json["id"]

    added = []

    for exercise_id in exercises:
        response = client.post(
            f"/api/workouts/{workout_id}/exercises",
            json={
                "exercise_id": exercise_id,
                "description": "3 sets"
            },
            headers=auth_headers
        )
        added.append(response.json["id"])

    response = client.delete(
        f"/api/workout-exercises/{added[2]}",
        headers=auth_headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/workouts/{workout_id}/exercises",
        headers=auth_headers
    )

    assert [
        exercise["position"]
        for exercise in get_response.json
    ] == [1, 2]


def test_different_users_can_use_their_own_exercises_in_their_own_workouts(client, auth_headers, second_auth_headers):
    first_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=auth_headers)

    second_workout = client.post("/api/workouts", json={
        "name": "Push Day"
    }, headers=second_auth_headers)

    first_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=auth_headers)

    second_exercise = client.post("/api/exercises", json={
        "name": "Bench Press",
        "category": "Chest"
    }, headers=second_auth_headers)

    first_response = client.post(
        f"/api/workouts/{first_workout.json['id']}/exercises",
        json={
            "exercise_id": first_exercise.json["id"],
            "description": "4 sets"
        },
        headers=auth_headers
    )

    second_response = client.post(
        f"/api/workouts/{second_workout.json['id']}/exercises",
        json={
            "exercise_id": second_exercise.json["id"],
            "description": "3 sets"
        },
        headers=second_auth_headers
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201