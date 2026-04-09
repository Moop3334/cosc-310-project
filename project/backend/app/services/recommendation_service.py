from collections import Counter
from app.services.order_service import list_orders
from app.services.restaurant_service import list_restaurants
from fastapi import HTTPException

COMPLETED_STATUSES = ["Completed", "Delivered", "Cancelled"]

def get_recommended_restaurants_for_user(user_id: int):
    orders = list_orders()

    past_orders = [
        order for order in orders
        if order.user_id == user_id and order.status in COMPLETED_STATUSES
    ]

    if not past_orders:
        return []

    restaurant_counts = Counter(order.restaurant_id for order in past_orders)

    restaurants = list_restaurants()
    restaurant_map = {restaurant.id: restaurant for restaurant in restaurants}

    recommendations = []
    for restaurant_id, count in restaurant_counts.most_common(1):
        restaurant = restaurant_map.get(restaurant_id)
        if restaurant:
            recommendations.append({
                "restaurant_id": restaurant.id,
                "restaurant_name": restaurant.name,
                "address": restaurant.address,
                "order_count": count
            })

    return recommendations