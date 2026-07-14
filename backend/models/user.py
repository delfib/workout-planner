from datetime import datetime
from models import db
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    workouts = db.relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    exercises = db.relationship("Exercise", back_populates="user", cascade="all, delete-orphan")