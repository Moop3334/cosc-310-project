from fastapi import HTTPException
from app.schema.user import User
from app.repositories.user_repos import load_all_users, save_all_users, find_user_by_username, find_user_by_email


def list_users():
    result = []

    for u in load_all_users():
        user = User(
            user_id=u["user_id"],
            name=u["name"],
            phone_number=u["phone_number"],
            address=u["address"],
            username=u["username"],
            email=u["email"],
            password_hash=u["password_hash"], #not hashed password at this moment
            role=u.get("role"),
            is_active=u["is_active"],
            editable_restaurants=u.get("editable_restaurants", [])
        )
        result.append(user)

    return result


def register_user(payload):
    username = payload.username.strip()
    email = str(payload.email).strip().lower()

    if find_user_by_username(username) is not None:
        raise HTTPException(status_code=409, detail="Username already exists")

    if find_user_by_email(email) is not None:
        raise HTTPException(status_code=409, detail="Email already exists")

    users = load_all_users()
    new_id = len(users) + 1

    user = User(
        user_id=new_id,
        name=payload.name.strip(),
        phone_number=payload.phone_number.strip(),
        address=payload.address.strip(),
        username=username,
        email=email,
        password_hash=payload.password_hash,
        role=payload.role,
        is_active=True,
        editable_restaurants=[]
    )

    users.append(user.model_dump())
    save_all_users(users)

    return user


def login_user(payload):
    username = payload.username.strip()
    user = find_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user["is_active"] == False:
        raise HTTPException(status_code=403, detail="User account is inactive")

    if user["password_hash"] != payload.password_hash:
        raise HTTPException(status_code=401, detail="Invalid password")

    return "Login successful for user '" + user["username"] + "'"


def get_user_by_username(username):
    user = find_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User(
        user_id=user["user_id"],
        name=user["name"],
        phone_number=user["phone_number"],
        address=user["address"],
        username=user["username"],
        email=user["email"],
        password_hash=user["password_hash"],
        role=user.get("role"),
        is_active=user["is_active"],
        editable_restaurants=user.get("editable_restaurants", [])
    )