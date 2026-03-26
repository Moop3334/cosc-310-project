from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
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

def create_token(data: dict, expires: timedelta | None = None):
    encode = data.copy()
    if expires:
        expire = datetime.now(timezone.utc) + expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    encode.update({"exp": expire})
    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def auth_user(username:str, password:str):
    user = get_user() #get user from storage, should return an error if user isn't found
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(username=username)
    except HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}):
        raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user = get_user()
    if user is None:
        raise HTTPException(401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

async def get_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def login_for_access(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub":user.username}, 
        expires=access_token_expires
    )
    return Token(access_token, "bearer")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")