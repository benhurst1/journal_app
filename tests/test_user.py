from lib.user.user import User
from unittest.mock import Mock


def test_user_creation():
    user = User(1, "username", "password", "email@email.com")
    assert user.id == 1
    assert user.username == "username"
    assert user.password == "password"
    assert user.email == "email@email.com"
