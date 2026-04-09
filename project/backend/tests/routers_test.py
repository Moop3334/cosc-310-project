import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from datetime import time
from app.routers.restaurant_routers import router as restaurant_router, menu_router
from app.routers.cart_routers import router as cart_router
from app.services.restaurant_service import list_restaurants
from app.services.menu_service import list_menu, get_menu_item_by_id, update_menu_item
from app.routers.order_routers import router as order_router
from app.services.order_service import list_orders, get_specific_order, checkout, update_order_status, delete_specific_order, complete_an_order
from app.services.cart_service import add_to_cart, get_cart, get_or_create_cart, remove_from_cart, remove_all_from_cart, clear_cart

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
        'description': 'Japanese Curry'
        }, 
    {
        'restaurant_id':4,
        'id': '2',
        'item_name': 'Chicken', 
        'price': '10.0', 
        'description': 'Mmmm chicken'
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
        'description': 'Japanese Curry'
        }, 
    {
        'restaurant_id':4,
        'id': '2',
        'item_name': 'Chicken', 
        'price': '10.0', 
        'description': 'Mmmm chicken'
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
        'description': 'Japanese Curry'
        }, 
    {
        'restaurant_id':4,
        'id': 2,
        'item_name': 'Chicken', 
        'price': 10.0, 
        'description': 'Mmmm chicken'
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
      "description": "Japanese Curry"
    },
    {
      "id": 2,
      "restaurant_id": 1,
      "item_name": "Chicken",
      "price": 10.0,
      "description": "Mmmm chicken"
    }
  ]
})

temp_cart_item_1 = {
  "item_id": 1,
  "item_name": "Curry",
  "quantity": 1,
  "price": 12.99
}

temp_cart_item_2 = {
  "item_id": 2,
  "item_name": "Chicken",
  "quantity": 2,
  "price": 10.00
}

temp_cart_checked_out = {
  "id": 6,
  "user_id": 1,
  "restaurant_id": 1,
  "items": [
    {
      "item_id": 1,
      "item_name": "Curry",
      "quantity": 1,
      "price": 12.99
    },
    {
      "item_id": 2,
      "item_name": "Chicken",
      "quantity": 2,
      "price": 10
    }
  ],
  "total_price": 37.639500000000005,
  "creation_date": "2026-04-08T06:20:52.881000",
  "status": "Pending Approval"
}

app = FastAPI()

app.include_router(restaurant_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(cart_router)

client = TestClient(app)

#Shopping cart router tests

def test_add_item():
    response = client.post("/cart/1/add", params={"restaurant_id":"1"}, json=temp_cart_item_1)
    assert response.status_code == 200
    assert response.json()["message"] == "Item 'Curry' (qty: 1) added to cart"
    assert temp_cart_item_1 == get_cart(1).items[0].model_dump()

def test_add_multipule_items():
    response = client.post("/cart/1/add", params={"restaurant_id":"1"}, json=temp_cart_item_2)
    assert response.status_code == 200
    assert response.json()["message"] == "Item 'Chicken' (qty: 2) added to cart"
    assert temp_cart_item_2 == get_cart(1).items[1].model_dump()

def test_view_cart():
    response = client.get("/cart/1")
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == 1 and body["restaurant_id"] == 1
    items = body["items"]
    assert items[0] == temp_cart_item_1
    assert items[1] == temp_cart_item_2
    assert body["total"] == 32.99

def test_remove_one():
    response = client.delete("/cart/1/items/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Item 2 removed from cart"
    tmp_cart_2 = temp_cart_item_2.copy()
    tmp_cart_2["quantity"] = 1
    assert tmp_cart_2 == get_cart(1).items[1].model_dump()

def test_remove_all():
    client.post("/cart/1/add", params={"restaurant_id":"1"}, json=temp_cart_item_1)

    response = client.delete("/cart/1/items/1/clear")
    assert response.status_code == 200
    assert response.json()["message"] == "Item 1 removed from cart"
    assert len(get_cart(1).items) == 1
    assert temp_cart_item_1 not in get_cart(1).items

def test_clear_cart():
    response = client.delete("/cart/1/clear")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart cleared successfully"
    assert get_cart(1) is None

def test_cart_summary():
    client.post("/cart/1/add", params={"restaurant_id":"1"}, json=temp_cart_item_1)
    client.post("/cart/1/add", params={"restaurant_id":"1"}, json=temp_cart_item_2)

    response = client.get("/cart/1/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == 1 and body["restaurant_id"] == 1
    assert body["item_count"] == 2 and body["items"] == [temp_cart_item_1, temp_cart_item_2]
    assert body["subtotal"] == 32.99 and body["tax"] == 1.65 and body["delivery_fee"] == 3 and body["total_with_fees"] == 37.64 #TODO: Change magic numbers

#Order Router Tests TODO: MAKE MORE ORDER TESTS CHIP

def test_checkout():
    response = client.post("/orders/1/checkout")
    assert response.status_code == 200 #Probably should be 201
    temp_cart_checked_out["creation_date"] = response.json()["creation_date"]
    assert response.json() == temp_cart_checked_out

def test_list_orders():
    response = client.get("/orders")
    orders = list_orders()
    assert response.status_code == 200
    for o in range(1, len(response.json())):
        tmp = orders[o].__dict__
        for i in range(0, len(tmp["items"])):
            tmp["items"][i] = tmp["items"][i].__dict__
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
    response = client.put("/restaurants/1", json=restaurant_1)
    assert response.status_code == 200
    assert response.json() == restaurant_1
    client.post("/restaurants/1", json=restaurant_1)

def test_update_invalid_restaurant():
    response = client.put("/restaurants/999", json=restaurant_1)
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant '999' not found"}

def test_update_restaurant_invalid_input():
  response = client.put("/restaurants/1", json={
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
      "description": "Japanese Curry"
    },
    {
      "id": 2,
      "restaurant_id": 1,
      "item_name": "Chicken",
      "price": 10.0,
      "description": "Mmmm chicken"
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
  "description": "Test"
}
invalid_menu_creator = {
  "item_name": "",
  "restaurant_id": -1,
  "price": 0,
  "description": ""
}
invalid_restaurant_menu_creator = {
  "item_name": "Test",
  "restaurant_id": 99,
  "price": 19.99,
  "description": "Testing"
}

def test_list_menu():
    response = client.get("/restaurants/1/menu")
    menu = list_menu(1)
    assert response.status_code == 200
    for m in range(1, len(response.json())):
        assert menu[m].__dict__ == response.json()[m]

def test_search_menu():
    response = client.get("/restaurants/1/menu", params={"name":"Curry"})
    curry = list_menu(1)[0]
    assert response.status_code == 200
    assert response.json()[0] == curry.__dict__

def test_blank_search_menu():
    response = client.get("/restaurants/1/menu", params={"name":""})
    menu = list_menu(1)
    assert response.status_code == 200
    for m in range(1, len(response.json())):
        assert menu[m].__dict__ == response.json()[m]

def test_search_menu_not_found():
    response = client.get("/restaurants/1/menu", params={"name":"Nutrition Brick"})
    assert response.status_code == 200
    assert response.json() == []

def test_list_invalid_restaurant_menu():
    response = client.get("/restaurants/99/menu")
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_get_menu_item_by_id():
    response = client.get("/restaurants/1/menu/1")
    menu_item = get_menu_item_by_id(1,1)
    assert response.status_code == 200
    assert menu_item.__dict__ == response.json()

def test_get_invalid_menu_item():
    response = client.get("/restaurants/1/menu/99")
    assert response.status_code == 404
    assert response.json() == {"detail":"Menu Item 99 not found for restaurant 1"}

def test_get_menu_item_from_invalid_restaurant():
    response = client.get("/restaurants/99/menu/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_create_menu_item():
    response = client.post("/restaurants/1/menu", json=test_menu_creator)
    assert response.status_code == 201
    test_menu_creator["id"] = 3
    assert response.json() == test_menu_creator

def test_create_invalid_restaurant_menu_item():
    response = client.post("/restaurants/99/menu", json=invalid_restaurant_menu_creator)
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_create_menu_item_invalid_input():
    response = client.post("/restaurants/1/menu", json=invalid_menu_creator)
    assert response.status_code == 422
    details = response.json()["detail"]
    assert details[0]["msg"] == "String should have at least 1 character"
    assert details[1]["msg"] == "Input should be greater than or equal to 0"
    assert details[2]["msg"] == "Input should be greater than 0"
    assert details[3]["msg"] == "String should have at least 1 character"

def test_update_menu_item():
    item = get_menu_item_by_id(1,1)
    response = client.post("/restaurants/1/menu/1", json=test_menu_creator)
    assert response.status_code == 201
    test_menu_creator["id"] = 1
    assert response.json() == test_menu_creator
    update_menu_item(1,1, item)

def test_update_invalid_restaurant_menu_item():
    response = client.post("/restaurants/99/menu/1", json=invalid_restaurant_menu_creator)
    assert response.status_code == 404
    assert response.json() == {"detail":"Unable to find a restaurant with id 99"}

def test_update_invalid_menu_item():
    response = client.post("/restaurants/1/menu/99", json=test_menu_creator)
    assert response.status_code == 404
    assert response.json() == {"detail":"Menu Item 99 not found for restaurant 1"}

def test_update_menu_item_invalid_input():
    response = client.post("/restaurants/1/menu", json=invalid_menu_creator)
    assert response.status_code == 422
    details = response.json()["detail"]
    assert details[0]["msg"] == "String should have at least 1 character"
    assert details[1]["msg"] == "Input should be greater than or equal to 0"
    assert details[2]["msg"] == "Input should be greater than 0"
    assert details[3]["msg"] == "String should have at least 1 character"

def test_delete_menu_item():
    try:
        response = client.delete("/restaurants/1/menu/3")
        assert response.status_code == 200
    except HTTPException:
        pytest.fail("Restaurant does not exist")

def test_delete_invalid_menu_item():
    response = client.delete("/restaurants/1/menu/3")
    assert response.status_code == 404
    assert response.json() == {"detail":"Menu Item 3 not found for restaurant 1"}
