from datetime import datetime
from app.schema.user import User
from app.schema.order import OrderStatus
from app.schema.orderDetail import OrderItem

# test data
user = User(1, "John Smith", "123-456-7890", "123 Main St")
items = [
    OrderItem(item="Curry", quantity=2),
    OrderItem(item="Chicken", quantity=1)
]


# getter tests
def test_id():
    assert user.get_id() == 1

def test_name():
    assert user.get_name() == "John Smith"

def test_phone():
    assert user.get_phone_number() == "123-456-7890"

def test_address():
    assert user.get_address() == "123 Main St"

def test_default_role():
    assert user.get_role() == None

def test_empty_editable_restaurants():
    assert user.get_editable_restaurants() == []


# role tests
def test_set_admin_role():
    u = User(2, "Jane Doe", "987-654-3210", "456 Oak Ave", role="admin")
    assert u.get_role() == "admin"

def test_set_customer_role():
    u = User(3, "Adam Walker", "555-555-5555", "789 Pine St", role="customer")
    assert u.get_role() == "customer"


# editable restaurant tests
def test_add_one_restaurant():
    u = User(4, "Seth Brown", "111-222-3333", "321 Elm St")
    u.editable_restaurants.append("Pizza Place")
    assert "Pizza Place" in u.get_editable_restaurants()

def test_add_multiple_restaurants():
    u = User(5, "Charlie Williams", "444-555-6666", "654 Maple Ave")
    u.editable_restaurants.append("Pizza Place")
    u.editable_restaurants.append("Burger Joint")
    assert len(u.get_editable_restaurants()) == 2


# create order tests
def test_create_order_ok():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", items)
    assert o != None
    assert o.user == "John Smith"
    assert o.restaurant == "Test Restaurant"
    assert len(o.items) == 2

def test_create_order_with_empty_list():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", [])
    assert o == None

def test_create_order_with_none():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", None)
    assert o == None

def test_order_default_st():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", items)
    assert o.status == OrderStatus.PENDING

def test_order_has_time():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", items)
    assert type(o.creation_date) == datetime


# cancel order tests
def test_cancel_success():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", items)
    r = u.cancel_order(o)
    assert r == True
    assert o.status == OrderStatus.CANCELLED

def test_cancel_none_order():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    assert u.cancel_order(None) == False

def test_cancel_delivered_order():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", items)
    o.status = OrderStatus.DELIVERED
    r = u.cancel_order(o)
    assert r == False

def test_cancel_twice():
    u = User(1, "John Smith", "123-456-7890", "123 Main St")
    o = u.create_order(1, "Test Restaurant", items)
    u.cancel_order(o)
    r = u.cancel_order(o)
    assert r == True