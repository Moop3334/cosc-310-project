import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200


def test_signup_user():
    payload = {
        "name": "Will Smith",
        "phone_number": "123-456-799",
        "address": "Okanagan",
        "username": "smith1",
        "email": "smith@example.com",
        "password_hash": "pass123",
        "role": "customer"
    }

    response = client.post("/users/signup", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "smith1"
    assert data["email"] == "smith@example.com"


def test_login_user():
    payload = {
        "username": "smith1",
        "password_hash": "pass123"
    }

    response = client.post("/users/login", json=payload)
    assert response.status_code == 200