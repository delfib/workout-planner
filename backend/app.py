from flask import Flask
from config import Config
from flask_cors import CORS
from routes.auth import auth_bp
from routes.user import user_bp
from routes.exercise import exercise_bp
from routes.workout import workout_bp
from routes.workout_day import workout_day_bp
from routes.workout_exercise import workout_exercise_bp

from extensions import db, migrate, bcrypt, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(exercise_bp, url_prefix="/api/exercises")
    app.register_blueprint(workout_bp, url_prefix="/api/workouts")
    app.register_blueprint(workout_day_bp, url_prefix="/api/workout-days")
    app.register_blueprint(workout_exercise_bp, url_prefix="/api")

    @app.route("/api/health")
    def health():
        return {"message": "API is running"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)