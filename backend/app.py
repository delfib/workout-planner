from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.route("/api/health")
def health():
    return {"message": "API is running"}


if __name__ == "__main__":
    app.run(debug=True)