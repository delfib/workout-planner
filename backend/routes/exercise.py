from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import db
from models.exercise import Exercise, ExerciseCategory

exercise_bp = Blueprint("exercise", __name__)


@exercise_bp.route("", methods=["POST"])
@jwt_required()
def create_exercise():
    user_id = get_jwt_identity()

    data = request.get_json()

    name = data.get("name", "").strip()
    category = data.get("category", "").strip()

    if not name or not category:
        return jsonify({"error": "Missing fields"}), 400

    existing_exercise = Exercise.query.filter(
        Exercise.user_id == int(user_id),
        func.lower(Exercise.name) == name.lower()
    ).first()

    if existing_exercise:
        return jsonify({"error": "Exercise already exists"}), 400

    category = next(
        (
            c for c in ExerciseCategory
            if c.value.lower() == category.lower()
        ),
        None
    )

    if category is None:
        return jsonify({"error": "Invalid category"}), 400

    new_exercise = Exercise(
        user_id=int(user_id),
        name=name,
        category=category
    )

    db.session.add(new_exercise)
    db.session.commit()

    return jsonify({
        "id": new_exercise.id,
        "name": new_exercise.name,
        "category": new_exercise.category.value
    }), 201