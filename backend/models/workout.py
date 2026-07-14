from models import db
from datetime import datetime

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="workouts")

    days = db.relationship("WorkoutDay", back_populates="workout", cascade="all, delete-orphan")

    exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")
    
    __table_args__ = (db.UniqueConstraint("user_id", "name", name="unique_user_workout_name"),)