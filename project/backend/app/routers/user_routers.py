from typing import List
from fastapi import APIRouter
from app.schema.user import User, UserCreate, UserLogin
from app.services.user_service import *

router = APIRouter(
    prefix="/users",
    tags=["users"] 
)

@router.get("")
def get_users():
    return list_users()


@router.post("/signup")
def signup(payload: UserCreate):
    return register_user(payload)


@router.post("/login")
def login(payload: UserLogin):
    return login_user(payload)


@router.put("/id/{user_id}")
def update_user_by_id_route(user_id: int, payload: dict):
    """Update a user by user_id."""
    return update_user_by_id(user_id, payload)


@router.delete("/id/{user_id}")
def delete_user_route(user_id: int):
    """Delete a user by user_id."""
    return delete_user_by_id(user_id)


@router.get("/{username}")
def get_user(username):
    return get_user_by_username(username)


@router.put("/{username}")
def update_user_route(username: str, payload: dict):
    return update_user(username, payload)