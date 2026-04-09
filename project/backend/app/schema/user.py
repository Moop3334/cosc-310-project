from pydantic import BaseModel, EmailStr
from typing import List, Optional


class User(BaseModel):
    user_id: int
    name: str
    phone_number: str
    address: str
    username: str
    email: EmailStr
    password_hash: str
    role: Optional[str] = None
    is_active: bool = True
    editable_restaurants: List[str] = []
    credit: int

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def can_login(self) -> bool:
        if not self.is_active:
            return False
        if self.username == "" or self.password_hash == "":
            return False
        return True


class UserCreate(BaseModel):
    name: str
    phone_number: str
    address: str
    username: str
    email: EmailStr
    password_hash: str
    role: Optional[str] = None
    credit: int


class UserLogin(BaseModel): #simple user login
    username: str
    password_hash: str