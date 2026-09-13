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


# optional parameters: ?category= and ?search=
@exercise_bp.route("", methods=["GET"])
@jwt_required()
def get_exercises():
    user_id = get_jwt_identity()

    category = request.args.get("category")
    search = request.args.get("search")

    query = Exercise.query.filter_by(
        user_id=int(user_id)
    )

    if category:
        category_enum = next(
            (
                c for c in ExerciseCategory
                if c.value.lower() == category.lower()
            ),
            None
        )

        if category_enum is None:
            return jsonify({"error": "Invalid category"}), 400

        query = query.filter_by(category=category_enum)

    if search:
        query = query.filter(
            Exercise.name.ilike(f"%{search}%")
        )

    exercises = query.order_by(Exercise.name).all()

    result = [
        {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category.value
        }
        for exercise in exercises
    ]

    return jsonify(result), 200


@exercise_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_exercise(id):
    user_id = get_jwt_identity()

    data = request.get_json()

    exercise = Exercise.query.filter_by(
        id=id,
        user_id=int(user_id)
    ).first()

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    name = data.get("name", "").strip()
    category = data.get("category")

    if not name and not category:
        return jsonify({"error": "No fields to update"}), 400

    if name:
        existing_exercise = Exercise.query.filter(
            Exercise.user_id == int(user_id),
            Exercise.id != exercise.id,
            func.lower(Exercise.name) == name.lower()
        ).first()

        if existing_exercise:
            return jsonify({"error": "Exercise already exists"}), 400

        exercise.name = name

    if category:
        category = category.strip()

        category_enum = next(
            (
                c for c in ExerciseCategory
                if c.value.lower() == category.lower()
            ),
            None
        )

        if category_enum is None:
            return jsonify({"error": "Invalid category"}), 400

        exercise.category = category_enum

    db.session.commit()

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category.value
    }), 200



@exercise_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_exercise(id):
    user_id = get_jwt_identity()

    exercise = Exercise.query.filter_by(
        id=id,
        user_id=int(user_id)
    ).first()

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200