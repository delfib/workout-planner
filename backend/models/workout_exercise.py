from models import db
class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)

    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    description = db.Column(db.String(255), nullable=False)

    position = db.Column(db.Integer, nullable=False)

    workout = db.relationship("Workout", back_populates="exercises")

    exercise = db.relationship("Exercise", back_populates="workouts")

    __table_args__ = (db.UniqueConstraint("workout_id", "exercise_id", name="unique_workout_exercise"),
    db.UniqueConstraint("workout_id", "position", name="unique_workout_position"),)