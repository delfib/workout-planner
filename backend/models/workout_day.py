from models import db
from enum import Enum

class WeekDay(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class WorkoutDay(db.Model):
    __tablename__ = "workout_days"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)

    day_of_week = db.Column(db.Enum(WeekDay), nullable=False)

    workout = db.relationship("Workout", back_populates="days")