from pathlib import Path
import csv

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.csv"


def load_all_users():
    if not DATA_PATH.exists():
        return []

    result = []

    with open(DATA_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["user_id"] = int(row["user_id"])

            if row["is_active"] == "True":
                row["is_active"] = True
            else:
                row["is_active"] = False

            if row["editable_restaurants"] == "":
                row["editable_restaurants"] = []
            else:
                row["editable_restaurants"] = row["editable_restaurants"].split(";")

            result.append(row)

    return result


def save_all_users(users):
    fields = [
        "user_id",
        "name",
        "phone_number",
        "address",
        "username",
        "email",
        "password_hash",
        "role",
        "is_active",
        "editable_restaurants"
    ]

    if not DATA_PATH.parent.exists():
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for user in users:
            temp = dict(user)
            temp["editable_restaurants"] = ";".join(temp["editable_restaurants"])
            writer.writerow(temp)


def find_user_by_username(username):
    users = load_all_users()

    for user in users:
        if user["username"] == username:
            return user

    return None


def find_user_by_email(email):
    users = load_all_users()

    for user in users:
        if user["email"] == email:
            return user

    return None