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


@router.get("/{username}")
def get_user(username):
    return get_user_by_username(username)


@router.post("/signup")
def signup(payload: UserCreate):
    return register_user(payload)


@router.post("/login")
def login(payload: UserLogin):
    return login_user(payload)