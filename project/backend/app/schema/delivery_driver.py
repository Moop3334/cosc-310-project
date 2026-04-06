from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class DeliveryDriver(BaseModel):
    driver_id: int
    name: str
    phone_number: str
    drivername: str
    email: EmailStr
    password_hash: str
    vehicle_type: Optional[str] = None
    is_active: bool = True
    completed_orders: List[int] = Field(default_factory=list)

    def get_id(self):
        return self.driver_id

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_drivername(self):
        return self.drivername

    def get_email(self):
        return self.email

    def get_vehicle_type(self):
        return self.vehicle_type

    def get_is_active(self):
        return self.is_active

    def can_login(self):
        return self.is_active and self.username != "" and self.password_hash != ""

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True