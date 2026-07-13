from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import db
from models.workout import Workout


workout_bp = Blueprint("workout",__name__)


@workout_bp.route("", methods=["POST"])
@jwt_required()
def create_workout():
    user_id = get_jwt_identity()

    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Missing fields"}), 400

    existing_workout = Workout.query.filter(
        Workout.user_id == int(user_id),
        func.lower(Workout.name) == name.lower()
    ).first()

    if existing_workout:
        return jsonify({"error": "Workout already exists"}), 400
    
    new_workout = Workout(
        user_id=int(user_id),
        name=name
    )

    db.session.add(new_workout)
    db.session.commit()

    return jsonify({
        "id": new_workout.id,
        "name": new_workout.name
    }), 201


@workout_bp.route("", methods=["GET"])
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()


    workouts = Workout.query.filter_by(
        user_id=int(user_id)
    ).order_by(Workout.name).all()

    result = [
        {
            "id": workout.id,
            "name": workout.name,
        }
        for workout in workouts
    ]

    return jsonify(result), 200


@workout_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_workout(id):
    user_id = get_jwt_identity()

    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Missing fields"}), 400

    workout = Workout.query.filter_by(
        id=id,
        user_id=int(user_id)
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    existing_workout = Workout.query.filter(
        Workout.user_id == int(user_id),
        func.lower(Workout.name) == name.lower(),
        Workout.id != id
    ).first()

    if existing_workout:
        return jsonify({"error": "Workout already exists"}), 400

    workout.name = name

    db.session.commit()

    return jsonify({
        "id": workout.id,
        "name": workout.name
    }), 200


@workout_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_workout(id):
    user_id = get_jwt_identity()

    workout = Workout.query.filter_by(
        id=id,
        user_id=int(user_id)
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully"
    }), 200