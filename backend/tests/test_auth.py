def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}


def test_register_missing_fields(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Missing fields"}


def test_register_duplicate_email(client, registered_user):
    response = client.post("/api/auth/register", json={
        "username": "user2",
        "email": registered_user["email"],
        "password": "password456"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Email already exists"}


def test_register_duplicate_username(client, registered_user):
    response = client.post("/api/auth/register", json={
        "username": registered_user["username"],
        "email": "second@example.com",
        "password": "password456"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Username already exists"}


def test_login_success(client, registered_user):
    response = client.post("/api/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })

    assert response.status_code == 200
    assert response.json["message"] == "Login successful"
    assert "token" in response.json
    assert response.json["user"]["username"] == registered_user["username"]
    assert response.json["user"]["email"] == registered_user["email"]


def test_login_invalid_password(client, registered_user):
    response = client.post("/api/auth/login", json={
        "email": registered_user["email"],
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_login_nonexistent_user(client):
    response = client.post("/api/auth/login", json={
        "email": "doesnotexist@example.com",
        "password": "password123"
    })

    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={
        "email": "test@example.com"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Missing email or password"}


def test_me_requires_authentication(client):
    response = client.get("/api/user/me")

    assert response.status_code == 401


def test_me_returns_authenticated_user(client, registered_user, auth_headers):
    response = client.get("/api/user/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json["username"] == registered_user["username"]
    assert response.json["email"] == registered_user["email"]