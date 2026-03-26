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
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "pass123"
    }

    response = client.post("/users/signup", json=payload)
    assert response.status_code == 201


def test_login_user():
    payload = {
        "username": "Will Smith",
        "password": "pass123"
    }

    response = client.post("/users/login", json=payload)
    assert response.status_code == 200