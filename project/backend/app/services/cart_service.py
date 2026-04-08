from typing import Dict, List
from app.schema.shopping_cart import CartItem, ShoppingCart
from app.services.payment_service import calculate_subtotal

#TODO: Throw errors if cart/user doesn't exist
# In-memory store, easier to implement than persistent storage
active_carts: Dict[int, ShoppingCart] = {}

#Returns cart if exists or creates new cart if it doesn't
def get_or_create_cart(user_id: int, restaurant_id: int) -> ShoppingCart:
    if user_id not in active_carts:
        active_carts[user_id] = ShoppingCart(
            user_id=user_id,
            restaurant_id=restaurant_id,
            items=[],
            total=1.0
        )
    return active_carts[user_id]

#Adds item to cart and updates cart subtotal
def add_to_cart(user_id: int, restaurant_id: int, item: CartItem):
    cart = get_or_create_cart(user_id, restaurant_id)
    
    existing_item = next((i for i in cart.items if i.item_id == item.item_id), None)
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        cart.items.append(item)
    
    cart.total = calculate_subtotal(cart.items)

def remove_from_cart(user_id: int, item_id: int):
    if user_id in active_carts:
        cart = active_carts[user_id]
        for i in cart.items:
            if i.item_id == item_id:
                i.quantity -= 1
            if i.quantity <= 0:
                cart.items.remove(i)
        cart.total = calculate_subtotal(cart.items)
    else:
        raise IndexError(f"Error: cart not found for user {user_id}.")

def remove_all_from_cart(user_id: int, item_id: int):
    if user_id in active_carts:
        cart = active_carts[user_id]
        cart.items = [i for i in cart.items if i.item_id != item_id]
        cart.total = calculate_subtotal(cart.items)
    else:
        raise IndexError(f"Error: cart not found for user {user_id}")

def clear_cart(user_id: int):
    if user_id in active_carts:
        del active_carts[user_id]

def get_cart(user_id: int) -> ShoppingCart | None:
    return active_carts.get(user_id)