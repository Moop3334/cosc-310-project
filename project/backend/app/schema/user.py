from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.schema.order import Order


class User:
    def __init__(
        self,
        user_id: int,
        name: str,
        phone_number: str,
        address: str,
        username: str,
        email: str,
        password_hash: str,
        role: Optional[str] = None,
        is_active: bool = True,
    ) -> None:
        self.user_id = user_id
        self.name = name.strip()
        self.phone_number = phone_number.strip()
        self.address = address.strip()
        self.username = username.strip()
        self.email = email.strip().lower()
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active
        self.editable_restaurants: List[str] = []

    def get_id(self) -> int:
        return self.user_id

    def get_name(self) -> str:
        return self.name

    def get_phone_number(self) -> str:
        return self.phone_number

    def get_address(self) -> str:
        return self.address

    def get_username(self) -> str:
        return self.username

    def get_email(self) -> str:
        return self.email

    def get_role(self) -> Optional[str]:
        return self.role

    def get_is_active(self) -> bool:
        return self.is_active

    def get_editable_restaurants(self) -> List[str]:
        return self.editable_restaurants

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def can_login(self) -> bool:
        return self.is_active and bool(self.username) and bool(self.password_hash)

    def create_order(
        self,
        order_id: int,
        restaurant_name: str,
        menu_items: list,
    ) -> Optional[Order]:
        if not self.is_active:
            return None
        if order_id is None or order_id < 0:
            return None
        if not restaurant_name or not restaurant_name.strip():
            return None
        if not menu_items:
            return None

        return Order(
            id=order_id,
            user=self.username,
            restaurant=restaurant_name.strip(),
            items=menu_items,
            creation_date=datetime.now(),
        )

    def cancel_order(self, order: Optional[Order]) -> bool:
        if order is None:
            return False

        current_status = getattr(order, "status", None)
        if current_status in {"delivered", "completed", "cancelled"}:
            return False

        order.status = "cancelled"
        return True