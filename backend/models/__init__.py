from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models import user, exercise, workout, workout_exercise, workout_day