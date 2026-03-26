import pytest
import json
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from datetime import time
from app.routers.restaurant_routers import router as restaurant_router, menu_router
from app.services.restaurant_service import list_restaurants
from app.services.menu_service import list_menu, get_menu_item_by_id, update_menu_item
from app.routers.order_routers import router as order_router
from app.services.order_service import list_orders, get_specific_order, save_an_order, update_order_status, delete_specific_order, complete_an_order
from app.schema.user import User, UserCreate, UserLogin
from app.services.auth_services import get_password_hash

@pytest.fixture(scope="module")
def client_1():
    with TestClient(app) as c:
      yield c

@pytest.fixture(scope="module")
def test_user():
    return UserLogin(
        username= "testuser",
        password_hash= "testpass"
    )

temp_restaurant_creator = {
    "name":"Test", 
    "address":"123 Road dr", 
    "open_times":['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00'], 
    "close_times":['21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00'],
    'menu':[
    {
        'restaurant_id':4,
        'id': '1',
        'item_name': 'Curry', 
        'price': '12.99', 
        'description': 'Japanese Curry', 
        'image': 'N/A'
        }, 
    {
        'restaurant_id':4,
        'id': '2',
        'item_name': 'Chicken', 
        'price': '10.0', 
        'description': 'Mmmm chicken', 
        'image': 'N/A'
    }
]
}

temp_invalid_restaurant_creator = {
    "name":"", 
    "address":"", 
    "open_times":['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00'], 
    "close_times":['21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00'],
    'menu':[
    {
        'restaurant_id':4,
        'id': '1',
        'item_name': 'Curry', 
        'price': '12.99', 
        'description': 'Japanese Curry', 
        'image': 'N/A'
        }, 
    {
        'restaurant_id':4,
        'id': '2',
        'item_name': 'Chicken', 
        'price': '10.0', 
        'description': 'Mmmm chicken', 
        'image': 'N/A'
    }
]
}

temp_restaurant = {
    "id":4,
    "name":"Test", 
    "address":"123 Road dr", 
    "open_times":['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00'], 
    "close_times":['21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00'],
    'menu':[
    {
        'restaurant_id':4,
        'id': 1,
        'item_name': 'Curry', 
        'price': 12.99, 
        'description': 'Japanese Curry', 
        'image': 'N/A'
        }, 
    {
        'restaurant_id':4,
        'id': 2,
        'item_name': 'Chicken', 
        'price': 10.0, 
        'description': 'Mmmm chicken', 
        'image': 'N/A'
    }
]
}

temp_order_creator = {
    "id": 8,
    "user_id": 8,
    "restaurant_id": 8,
    "item": "Curry",
    "price": 12.99,
    "status": "Pending Approval"
}

temp_order = {
    "id": 8,
    "user_id": 8,
    "restaurant_id": 8,
    "item": "Curry",
    "price": 12.99,
    "status": "Pending Approval"
}
restaurant_1 = ({
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
      "price": 10.0,
      "description": "Mmmm chicken",
      "image": "N/A"
    }
  ]
})

app = FastAPI()

app.include_router(restaurant_router)
app.include_router(menu_router)
app.include_router(order_router)

client = TestClient(app)

def test_login(client_1, test_user):
  response = client.post("/token", data=test_user)
  assert response.status_code == 200
  token = response.json()["access_token"]
  assert token is not None
  return token

#Order Router Tests

def test_list_orders():
    response = client.get("/orders")
    orders = list_orders()
    assert response.status_code == 200
    for o in range(1, len(response.json())):
        tmp = orders[o].__dict__
        tmp["creation_date"] = tmp["creation_date"].isoformat()
        assert tmp == response.json()[o]


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

def test_search_restaurant():
    response = client.get("/restaurants", params={"name":"Tester's Dinner"})
    assert response.status_code == 200
    assert response.json()[0] == restaurant_1

def test_blank_search_restaurant():
    response = client.get("/restaurants", params={"name":""})
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

def test_search_restaurant_not_found():
    response = client.get("/restaurants", params={"name":"Zanzibar"})
    assert response.status_code == 200
    assert response.json() == []

def test_create_restaurant():
    response = client.post("/restaurants", json=temp_restaurant_creator)
    assert response.status_code == 201
    assert response.json() == temp_restaurant

def test_create_restaurant_invalid_data():
    response = client.post("/restaurants", json=temp_invalid_restaurant_creator)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should have at least 1 character"
    assert response.json()["detail"][1]["msg"] == "String should have at least 1 character"
    assert response.json()["detail"][2]["msg"] == "List should have at least 7 items after validation, not 6"
    assert response.json()["detail"][3]["msg"] == "List should have at most 7 items after validation, not 8"

def test_create_existing_restaurant():
    respose = client.post("/restaurants", json={
    "name":"Tester's Dinner", 
    "address":"123 Road dr", 
    "open_times":['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00'], 
    "close_times":['21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00', '21:00:00'],
    'menu':[]})
    assert respose.status_code == 409
    assert respose.json() == {"detail": "Restaurant Already Exists"}

def test_get_restaurant_with_id():
    response = client.get("/restaurants/1")
    assert response.status_code == 200
    assert response.json() == restaurant_1

def test_get_invalid_restaurant_id():
    response = client.get("/restaurants/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant '99' not found"}

def test_update_restaurant():
    response = client.post("/restaurants/1", json=restaurant_1, data={"username":"testuser","password":"testpass"})
    assert response.status_code == 201
    assert response.json() == restaurant_1
    client.post("/restaurants/1", json=restaurant_1)

def test_update_invalid_restaurant():
    response = client.post("/restaurants/999", json=restaurant_1)
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant '999' not found"}

def test_update_restaurant_invalid_input():
  response = client.post("/restaurants/1", json={
  "name": "",
  "address": "",
  "open_times": [
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
      "price": 10.0,
      "description": "Mmmm chicken",
      "image": "N/A"
    }
  ]
})
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "String should have at least 1 character"
  assert response.json()["detail"][1]["msg"] == "String should have at least 1 character"
  assert response.json()["detail"][2]["msg"] == "List should have at least 7 items after validation, not 6"
  assert response.json()["detail"][3]["msg"] == "List should have at most 7 items after validation, not 8"

def test_delete_restaurant():
    try:
        response = client.delete("/restaurants/4")
        assert response.status_code == 200
    except HTTPException:
        pytest.fail("Restaurant does not exist")

def test_delete_invalid_restaurant():
    response = client.delete("/restaurants/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant '4' not found"}

#Menu Router Tests

test_menu_creator = {
  "item_name": "Test Burger",
  "restaurant_id": 1,
  "price": 10.00,
  "description": "Test",
  "image": "N/A"
}
invalid_menu_creator = {
  "item_name": "",
  "restaurant_id": -1,
  "price": 0,
  "description": "",
  "image": ""
}
invalid_restaurant_menu_creator = {
  "item_name": "Test",
  "restaurant_id": 99,
  "price": 19.99,
  "description": "Testing",
  "image": "N/A"
}

def test_list_menu():
    response = client.get("/1/menu")
    menu = list_menu(1)
    assert response.status_code == 200
    for m in range(1, len(response.json())):
        assert menu[m].__dict__ == response.json()[m]

def test_search_menu():
    response = client.get("/1/menu", params={"name":"Curry"})
    curry = list_menu(1)[0]
    assert response.status_code == 200
    assert response.json()[0] == curry.__dict__

def test_blank_search_menu():
    response = client.get("/1/menu", params={"name":""})
    menu = list_menu(1)
    assert response.status_code == 200
    for m in range(1, len(response.json())):
        assert menu[m].__dict__ == response.json()[m]

def test_search_menu_not_found():
    response = client.get("/1/menu", params={"name":"Nutrition Brick"})
    assert response.status_code == 200
    assert response.json() == []

def test_list_invalid_restaurant_menu():
    response = client.get("/99/menu")
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_get_menu_item_by_id():
    response = client.get("/1/menu/1")
    menu_item = get_menu_item_by_id(1,1)
    assert response.status_code == 200
    assert menu_item.__dict__ == response.json()

def test_get_invalid_menu_item():
    response = client.get("/1/menu/99")
    assert response.status_code == 404
    assert response.json() == {"detail":"Menu Item 99 not found for restaurant 1"}

def test_get_menu_item_from_invalid_restaurant():
    response = client.get("/99/menu/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_create_menu_item():
    response = client.post("/1/menu", json=test_menu_creator)
    assert response.status_code == 201
    test_menu_creator["id"] = 3
    assert response.json() == test_menu_creator

def test_create_invalid_restaurant_menu_item():
    response = client.post("/99/menu", json=invalid_restaurant_menu_creator)
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_create_menu_item_invalid_input():
    response = client.post("/1/menu", json=invalid_menu_creator)
    assert response.status_code == 422
    details = response.json()["detail"]
    assert details[0]["msg"] == "String should have at least 1 character"
    assert details[1]["msg"] == "Input should be greater than or equal to 0"
    assert details[2]["msg"] == "Input should be greater than 0"
    assert details[3]["msg"] == "String should have at least 1 character"
    assert details[4]["msg"] == "String should have at least 1 character"

def test_update_menu_item():
    item = get_menu_item_by_id(1,1)
    response = client.post("/1/menu/1", json=test_menu_creator)
    assert response.status_code == 201
    test_menu_creator["id"] = 1
    assert response.json() == test_menu_creator
    update_menu_item(1,1, item)

def test_update_invalid_restaurant_menu_item():
    response = client.post("/99/menu/1", json=invalid_restaurant_menu_creator)
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_update_invalid_menu_item():
    response = client.post("/1/menu/99", json=test_menu_creator)
    assert response.status_code == 404
    assert response.json() == {"detail":"Menu Item 99 not found for restaurant 1"}

def test_update_menu_item_invalid_input():
    response = client.post("/1/menu", json=invalid_menu_creator)
    assert response.status_code == 422
    details = response.json()["detail"]
    assert details[0]["msg"] == "String should have at least 1 character"
    assert details[1]["msg"] == "Input should be greater than or equal to 0"
    assert details[2]["msg"] == "Input should be greater than 0"
    assert details[3]["msg"] == "String should have at least 1 character"
    assert details[4]["msg"] == "String should have at least 1 character"

def test_delete_menu_item():
    try:
        response = client.delete("1/menu/3")
        assert response.status_code == 200
    except HTTPException:
        pytest.fail("Restaurant does not exist")

def test_delete_invalid_menu_item():
    response = client.delete("/1/menu/3")
    assert response.status_code == 404
    assert response.json() == {"detail":"Menu Item 3 not found for restaurant 1"}
