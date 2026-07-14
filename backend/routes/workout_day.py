from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.workout_day import WorkoutDay, WeekDay
from models.workout import Workout

workout_day_bp = Blueprint("workout-days", __name__)

DAY_ORDER = {
    WeekDay.MONDAY: 0,
    WeekDay.TUESDAY: 1,
    WeekDay.WEDNESDAY: 2,
    WeekDay.THURSDAY: 3,
    WeekDay.FRIDAY: 4,
    WeekDay.SATURDAY: 5,
    WeekDay.SUNDAY: 6,
}

@workout_day_bp.route("", methods=["POST"])
@jwt_required()
def create_workout_day():
    user_id = get_jwt_identity()

    data = request.get_json()

    workout_id = data.get("workout_id")
    day_of_week = data.get("day_of_week", "").strip()

    if not workout_id or not day_of_week:
        return jsonify({"error": "Missing fields"}), 400

    workout = Workout.query.filter_by(
        id=workout_id,
        user_id=int(user_id)
    ).first()

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    day_of_week = next(
        (
            d for d in WeekDay
            if d.value.lower() == day_of_week.lower()
        ),
        None
    )

    if day_of_week is None:
        return jsonify({"error": "Invalid day of the week"}), 400

    existing_workout_day = WorkoutDay.query.join(Workout).filter(
        Workout.user_id == int(user_id),
        WorkoutDay.day_of_week == day_of_week
    ).first()

    if existing_workout_day:
        return jsonify({"error": "A Workout is already assigned to this day"}), 400


    new_workout_day = WorkoutDay(
        workout_id=int(workout_id),
        day_of_week=day_of_week
    )

    db.session.add(new_workout_day)
    db.session.commit()

    return jsonify({
        "id": new_workout_day.id,
        "workout_id": new_workout_day.workout_id,
        "day_of_week": new_workout_day.day_of_week.value
    }), 201


@workout_day_bp.route("", methods=["GET"])
@jwt_required()
def get_workout_days():
    user_id = get_jwt_identity()

    workout_days = WorkoutDay.query.join(Workout).filter(
        Workout.user_id == int(user_id)
    ).all()

    workout_days.sort(key=lambda wd: DAY_ORDER[wd.day_of_week])
    
    result = [
        {
            "id": workout_day.id,
            "day_of_week": workout_day.day_of_week.value,
            "workout": {
                "id": workout_day.workout.id,
                "name": workout_day.workout.name
            }
        }
        for workout_day in workout_days
    ]

    return jsonify(result), 200