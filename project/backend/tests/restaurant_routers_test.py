import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.restaurant_routers import router as restaurant_router, menu_router

app = FastAPI()

app.include_router(restaurant_router)
app.include_router(menu_router)

client = TestClient(app)

def test_get_restaurant_with_id():
    response = client.get("/restaurants/1")
    assert response.status_code == 201
    assert response.json() == ({
  "id": 1,
  "name": "Tester's Dinner",
  "address": "123 Road dr",
  "open_times": [
    "09:00:00",
    "09:00:00",
    "09:00:00",
    "09:00:00",
    "09:00:00",
    "09:00:00",
    "09:00:00"
  ],
  "close_times": [
    "21:00:00",
    "21:00:00",
    "21:00:00",
    "21:00:00",
    "21:00:00",
    "21:00:00",
    "21:00:00"
  ],
  "menu": [
    {
      "id": 1,
      "restaurant_id": 1,
      "item_name": "Curry",
      "price": 12.99,
      "description": "Japanese Curry",
      "image": "N/A"
    },
    {
      "id": 2,
      "restaurant_id": 1,
      "item_name": "Chicken",
      "price": 10,
      "description": "Mmmm chicken",
      "image": "N/A"
    }
  ]
})

def test_get_invalid_restaurant_id():
    response = client.get("/restaurant/99")
    assert response.status_code == 404
    assert response.json() == {"detail": 'Not Found'}
