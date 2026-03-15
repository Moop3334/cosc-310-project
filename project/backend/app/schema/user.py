from typing import List
from app.schema.order import Order


class User():
    def __init__(self, user_id, name, phone_number, address, role=None):
        self.user_id = user_id
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.role = role
        self.editable_restaurants: List[str] = []

    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_address(self):
        return self.address

    def get_role(self):
        return self.role

    def get_editable_restaurants(self):
        return self.editable_restaurants

    def create_order(self, menu_items):
        if not menu_items:
            return None
        return Order(
            user=self,
            items=menu_items
        )

    def cancel_order(self, order):
        if order is None:
            return False
        if order.status == "delivered":
            return False
        order.status = "cancelled"
        return True