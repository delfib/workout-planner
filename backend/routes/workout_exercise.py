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

    if not exercise_id or not description or position is None:
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
    
    existing_position = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        position=position
    ).first()

    if existing_position:
        return jsonify({"error": "Position already occupied in workout"}), 400

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