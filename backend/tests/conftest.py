import pytest
from dotenv import load_dotenv

load_dotenv(".env.test")

from app import create_app
from config import TestingConfig
from extensions import db


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def registered_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }

    client.post("/api/auth/register", json=user_data)

    return user_data


@pytest.fixture
def second_user(client):
    user_data = {
        "username": "seconduser",
        "email": "second@example.com",
        "password": "password456"
    }

    client.post("/api/auth/register", json=user_data)

    return user_data


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post("/api/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })

    token = response.json["token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_auth_headers(client, second_user):
    response = client.post("/api/auth/login", json={
        "email": second_user["email"],
        "password": second_user["password"]
    })

    token = response.json["token"]

    return {"Authorization": f"Bearer {token}"}