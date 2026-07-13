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