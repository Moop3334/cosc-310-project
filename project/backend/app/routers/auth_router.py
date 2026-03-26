from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from app.schema.user import User
from app.schema.auth import Token, TokenData

SECRET_KEY = "c7a9de35495f7ec83b93c9f8817ad732d32352809b5e4dff15ace147564570fc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#Test/dummy user for testing auth functions while user data storage isn't implemented
test_user = User(
    user_id=1,
    name="Jane Doe",
    email="soldiertf2@valvesoftware.com",
    password_hash="$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
    role="Owner",
    is_active=True,
    editable_restaurants=[1]
)

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

#Dummy method until user data storage is implemented
def get_user():
    return test_user

def auth_user(username:str, password:str):
    user = get_user() #get user from storage, should return an error if user isn't found
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_token(data: dict, expires: timedelta | None = None):
    encode = data.copy()
    if expires:
        expire = datetime.now(timezone.utc) + expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    encode.update({"exp": expire})
    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

