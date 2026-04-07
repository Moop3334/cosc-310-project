from fastapi import APIRouter, HTTPException
from app.schema.order import CartItem
from app.services.cart_service import (
    add_to_cart, remove_from_cart, get_cart, clear_cart
)

router = APIRouter(prefix="/cart", tags=["cart"])

#TODO: Add more error handeling 
@router.post("/{user_id}/add")
def add_item(user_id: int, restaurant_id: int, item: CartItem):
    add_to_cart(user_id, restaurant_id, item)
    return {"message": "Item added to cart"}

@router.get("/{user_id}")
def view_cart(user_id: int):
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Error: cart not found")
    return cart

@router.delete("/{user_id}/items/{item_id}")
def remove_item(user_id: int, item_id: int):
    remove_from_cart(user_id, item_id)
    return {"message": "Item removed from cart"}

@router.delete("/{user_id}/clear")
def clear_user_cart(user_id: int):
    clear_cart(user_id)
    return {"message": "Cart cleared"}