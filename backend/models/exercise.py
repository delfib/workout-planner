from datetime import datetime
from enum import Enum

from models import db

class ExerciseCategory(Enum):
    CHEST = "Chest"
    BACK = "Back"
    LEGS = "Legs"
    SHOULDERS = "Shoulders"
    ARMS = "Arms"
    CORE = "Core"
    GLUTES = "Glutes"
    CARDIO = "Cardio"

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.Enum(ExerciseCategory), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="exercises")