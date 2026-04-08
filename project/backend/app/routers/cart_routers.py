from fastapi import APIRouter, HTTPException
from app.schema.shopping_cart import ShoppingCart, CartItem
from app.services.cart_service import (
    add_to_cart,
    remove_from_cart,
    remove_all_from_cart,
    get_cart,
    clear_cart
)

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/{user_id}/add", response_model=dict)
def add_item_to_cart(user_id: int, restaurant_id: int, item: CartItem):
    """Add an item to the user's shopping cart."""
    try:
        add_to_cart(user_id, restaurant_id, item)
        return {"message": f"Item '{item.item_name}' (qty: {item.quantity}) added to cart"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=ShoppingCart)
def view_cart(user_id: int):
    """View the user's shopping cart."""
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail=f"Error: cart not found for user {user_id}.")
    return cart


@router.delete("/{user_id}/items/{item_id}", response_model=dict)
def remove_item_from_cart(user_id: int, item_id: int):
    """Remove one of an item from the user's shopping cart."""
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail=f"Error: cart not found for user {user_id}")
    
    item_exists = any(item.item_id == item_id for item in cart.items)
    if not item_exists:
        raise HTTPException(status_code=404, detail=f"Error: item {item_id} not found in cart")
    
    remove_from_cart(user_id, item_id)
    return {"message": f"Item {item_id} removed from cart"}

@router.delete("/{user_id}/items/{item_id}/clear", response_model=dict) #There's 100% a better way to do this (ie pass the quantity of items you want when updating the cart or pass the no of items the user wants removed)
def remove_items_from_cart(user_id: int, item_id: int):                 #But this works and is simple enough to implement
    """Remove all of an item from the user's shopping cart."""
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail=f"Error: cart not found for user {user_id}")
    
    item_exists = any(item.item_id == item_id for item in cart.items)
    if not item_exists:
        raise HTTPException(status_code=404, detail=f"Error: item {item_id} not found in cart")
    
    remove_all_from_cart(user_id, item_id)
    return {"message": f"Item {item_id} removed from cart"}


@router.delete("/{user_id}/clear", response_model=dict)
def clear_user_cart(user_id: int):
    """Clear the user's shopping cart."""
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail=f"Error: cart not found for user {user_id}")
    
    clear_cart(user_id)
    return {"message": "Cart cleared successfully"}


@router.get("/{user_id}/summary", response_model=dict)
def get_cart_summary(user_id: int):
    """Get a summary of the user's shopping cart with pricing breakdown."""
    cart = get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail=f"Error: cart not found for user {user_id}")
    
    return {
        "user_id": cart.user_id,
        "restaurant_id": cart.restaurant_id,
        "item_count": len(cart.items),
        "items": cart.items,
        "subtotal": cart.total,
        "tax": round(cart.total * 0.05, 2),
        "delivery_fee": 3.00,
        "total_with_fees": round((cart.total * 1.05) + 3, 2)
    }