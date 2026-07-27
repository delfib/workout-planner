from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.workout_exercise import WorkoutExercise
from models.workout import Workout
from models.exercise import Exercise

workout_exercise_bp = Blueprint("workout_exercise", __name__)


@workout_exercise_bp.route("/workouts/<int:workout_id>/exercises", methods=["POST"])
@jwt_required()
def add_exercise_to_workout(workout_id):
    user_id = get_jwt_identity()

    data = request.get_json()

    exercise_id = data.get("exercise_id")
    description = data.get("description", "").strip()
    position = data.get("position")

    if not exercise_id or not description:
        return jsonify({"error": "Missing fields"}), 400

    workout = Workout.query.filter_by(
        id=workout_id,
        user_id=int(user_id)
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    exercise = Exercise.query.filter_by(
        id=exercise_id,
        user_id=int(user_id)
    ).first()

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    existing_exercise = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if existing_exercise:
        return jsonify({"error": "Exercise already added to workout"}), 400
    
    last_position = WorkoutExercise.query.filter_by(
        workout_id=workout_id
    ).count()

    position = last_position + 1

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        description=description,
        position=position
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify({
        "id": workout_exercise.id,
        "workout_id": workout_exercise.workout_id,
        "exercise_id": workout_exercise.exercise_id,
        "description": workout_exercise.description,
        "position": workout_exercise.position
    }), 201


@workout_exercise_bp.route("/workouts/<int:workout_id>/exercises", methods=["GET"])
@jwt_required()
def get_workout_exercises(workout_id):
    user_id = get_jwt_identity()

    workout = Workout.query.filter_by(
        id=workout_id,
        user_id=int(user_id)
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    workout_exercises = WorkoutExercise.query.filter_by(
        workout_id=workout_id
    ).order_by(
        WorkoutExercise.position
    ).all()

    result = [
        {
            "id": workout_exercise.id,
            "exercise": {
                "id": workout_exercise.exercise.id,
                "name": workout_exercise.exercise.name,
                "category": workout_exercise.exercise.category.value
            },
            "description": workout_exercise.description,
            "position": workout_exercise.position
        }
        for workout_exercise in workout_exercises
    ]

    return jsonify(result), 200


@workout_exercise_bp.route("/workout-exercises/<int:id>", methods=["PUT"])
@jwt_required()
def update_workout_exercise(id):
    user_id = get_jwt_identity()

    data = request.get_json() or {}

    exercise_id = data.get("exercise_id")
    description = data.get("description")
    position = data.get("position")

    if exercise_id is None and description is None and position is None:
        return jsonify({"error": "No fields to update"}), 400

    workout_exercise = db.session.get(WorkoutExercise, id)

    if not workout_exercise or workout_exercise.workout.user_id != int(user_id):
        return jsonify({"error": "Workout exercise not found"}), 404

    if exercise_id is not None:
        exercise = Exercise.query.filter_by(
            id=exercise_id,
            user_id=int(user_id)
        ).first()

        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        existing_exercise = WorkoutExercise.query.filter(
            WorkoutExercise.workout_id == workout_exercise.workout_id,
            WorkoutExercise.exercise_id == exercise_id,
            WorkoutExercise.id != id
        ).first()

        if existing_exercise:
            return jsonify({
                "error": "Exercise already added to workout"
            }), 400

        workout_exercise.exercise_id = exercise_id

    if description is not None:
        description = description.strip()

        if not description:
            return jsonify({"error": "Description cannot be empty"}), 400

        workout_exercise.description = description

    if position is not None:
        existing_position = WorkoutExercise.query.filter(
            WorkoutExercise.workout_id == workout_exercise.workout_id,
            WorkoutExercise.position == position,
            WorkoutExercise.id != id
        ).first()

        if existing_position:
            return jsonify({
                "error": "Position already occupied in workout"
            }), 400

        workout_exercise.position = position

    db.session.commit()

    return jsonify({
        "id": workout_exercise.id,
        "exercise": {
            "id": workout_exercise.exercise.id,
            "name": workout_exercise.exercise.name,
            "category": workout_exercise.exercise.category.value
        },
        "description": workout_exercise.description,
        "position": workout_exercise.position
    }), 200


@workout_exercise_bp.route("/workout-exercises/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_workout_exercise(id):
    user_id = get_jwt_identity()

    workout_exercise = db.session.get(WorkoutExercise, id)

    if not workout_exercise or workout_exercise.workout.user_id != int(user_id):
        return jsonify({"error": "Workout exercise not found"}), 404

    deleted_position = workout_exercise.position

    db.session.delete(workout_exercise)

    remaining = WorkoutExercise.query.filter(
        WorkoutExercise.workout_id == workout_exercise.workout_id,
        WorkoutExercise.position > deleted_position
    ).all()

    for exercise in remaining:
        exercise.position -= 1

    db.session.commit()


    return jsonify({
        "message": "Workout exercise deleted successfully"
    }), 200