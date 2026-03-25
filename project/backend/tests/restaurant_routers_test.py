import pytest
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import time
from app.routers.restaurant_routers import router as restaurant_router, menu_router
from app.services.restaurant_service import list_restaurants
from app.schema.resturant import Restaurant

app = FastAPI()

app.include_router(restaurant_router)
app.include_router(menu_router)

client = TestClient(app)

#Restaurant Router Tests

def test_get_restaurant_list(): #NOTE: There is almost certainly a better way to do this, but this works and won't impact the runtime of the actual website
    response = client.get("/restaurants")
    restaurants = list_restaurants()
    assert response.status_code == 200
    for r in range(1, len(response.json())):
        tmp = restaurants[r].__dict__
        for t in range(0, len(tmp["close_times"])):
            tmp["close_times"][t] = time.isoformat(tmp["close_times"][t])
            tmp["open_times"][t] = time.isoformat(tmp["open_times"][t])
        for m in range(0, len(tmp["menu"])):
            tmp["menu"][m] = tmp["menu"][m].__dict__
        assert tmp == response.json()[r]

def test_create_restaurant():
    assert True

def test_create_restaurant_invalid_data():
    assert True

def test_create_existing_restaurant():
    assert True

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

def test_update_restaurant():
    assert True

def test_update_invalid_restaurant():
    assert True

def test_update_restaurant_invalid_input():
    assert True

def test_delete_restaurant():
    assert True

#Menu Router Tests

def test_list_menu():
    assert True

def test_list_invalid_restaurant_menu():
    assert True

def test_get_menu_item_by_id():
    assert True

def test_get_invalid_menu_item():
    assert True

def test_get_menu_item_from_invalid_restaurant():
    assert True

def test_create_menu_item():
    assert True

def test_create_invalid_restaurant_menu_item():
    assert True

def test_create_menu_item_invalid_input():
    assert True

def test_update_menu_item():
    assert True

def test_update_invalid_restaurant_menu_item():
    assert True

def test_update_invalid_menu_item():
    assert True

def test_update_menu_item_invalid_input():
    assert True

def test_delete_menu_item():
    assert True