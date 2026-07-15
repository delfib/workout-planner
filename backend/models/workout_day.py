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

DAY_ORDER = {
    WeekDay.MONDAY: 0,
    WeekDay.TUESDAY: 1,
    WeekDay.WEDNESDAY: 2,
    WeekDay.THURSDAY: 3,
    WeekDay.FRIDAY: 4,
    WeekDay.SATURDAY: 5,
    WeekDay.SUNDAY: 6,
}
class WorkoutDay(db.Model):
    __tablename__ = "workout_days"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)

    day_of_week = db.Column(db.Enum(WeekDay), nullable=False)

    workout = db.relationship("Workout", back_populates="days")