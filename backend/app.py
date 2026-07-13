from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.user import user_bp

from extensions import db, migrate, bcrypt, jwt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")


@app.route("/api/health")
def health():
    return {"message": "API is running"}


if __name__ == "__main__":
    app.run(debug=True)