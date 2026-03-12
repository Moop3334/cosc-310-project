from app.schema.user import User


def test_user_getters():
    user = User(1, "Dave", "123-456-7890", "123 Main St")
    assert user.get_id() == 1
    assert user.get_name() == "Dave"
    assert user.get_phone_number() == "123-456-7890"
    assert user.get_address() == "123 Main St"


def test_cancel_order_none():
    user = User(1, "Yuya", "123-456-7890", "123 Main St")
    assert user.cancel_order(None) is False
