from lib.user.user_controller import UserController
import pytest, bcrypt
from lib.db_connection import DatabaseConnection


@pytest.fixture(scope="session")
def db_connection():
    dbconn = DatabaseConnection(test_mode=True)
    dbconn.execute(open("seeds/test_setup.sql", "r").read())
    dbconn.execute(open("seeds/setup.sql", "r").read())
    yield dbconn


def test_check_usernames(db_connection):
    uc = UserController(db_connection)
    assert uc._check_username("_user") == False
    assert uc._check_username("user_") == False
    assert uc._check_username("us") == False
    assert uc._check_username("ussssssssssssssss") == False
    assert uc._check_username("???") == False
    assert uc._check_username("username!") == False
    assert uc._check_username("@@@") == False
    assert uc._check_username("###") == False
    assert uc._check_username("$$$") == False
    assert uc._check_username("%%%") == False
    assert uc._check_username("^^^") == False
    assert uc._check_username("***") == False
    assert uc._check_username("(((") == False
    assert uc._check_username(")))") == False
    assert uc._check_username("---") == False
    assert uc._check_username("===") == False
    assert uc._check_username("+++") == False
    assert uc._check_username("{{{") == False
    assert uc._check_username("}}}") == False
    assert uc._check_username("|||") == False
    assert uc._check_username("\\\\\\") == False
    assert uc._check_username("[[[") == False
    assert uc._check_username("]]]") == False
    assert uc._check_username("'''") == False
    assert uc._check_username('"""') == False
    assert uc._check_username(";;;") == False
    assert uc._check_username(":::") == False
    assert uc._check_username("...") == False
    assert uc._check_username(",,,") == False
    assert uc._check_username("<<<") == False
    assert uc._check_username(">>>") == False
    assert uc._check_username("```") == False
    assert uc._check_username("~~~") == False
    assert uc._check_username("user") == True
    assert uc._check_username("user1") == True
    assert uc._check_username("user_1") == True
    assert uc._check_username("username1_ten_10") == True
    assert uc._check_username("username1_ten_101") == False


def test_check_password_min_req(db_connection):
    uc = UserController(db_connection)
    assert uc._check_password_min_req("password") == False
    assert uc._check_password_min_req("passwor") == False
    assert uc._check_password_min_req("password123") == False
    assert uc._check_password_min_req("########") == False
    assert uc._check_password_min_req("passssss123!") == False
    assert uc._check_password_min_req("!@#$1234") == False
    assert uc._check_password_min_req("Password123!") == True


def test_hash_password(db_connection):
    password = "password"
    hashed = UserController(db_connection)._hash_password(password)
    assert password != hashed


def test_hash_two_same_password(db_connection):
    password1 = "password"
    password2 = "password"
    hashed1 = UserController(db_connection)._hash_password(password1)
    hashed2 = UserController(db_connection)._hash_password(password2)
    assert hashed1 != hashed2
    assert password1 == password2
    assert bcrypt.checkpw(password1.encode(), hashed1) == True
    assert bcrypt.checkpw(password2.encode(), hashed2) == True


def test_add_user(db_connection):
    username = "user1"
    password = "Password1!"
    email = "email@email.com"
    uc = UserController(db_connection)
    uc.add_user(username, password, email)
    rows = db_connection.execute("SELECT * FROM users WHERE username = %s", [username])
    row = rows[0]

    assert row[0] == 1
    assert row[1] == username
    assert row[2] == email
    assert bcrypt.checkpw(password.encode(), bytes(row[3])) == True

    username2 = "user2"
    password2 = "Password1!"
    email2 = "email@email.net"
    uc.add_user(username2, password2, email2)
    rows = db_connection.execute("SELECT * FROM users WHERE username = %s", [username2])
    row = rows[0]

    assert row[0] == 2
    assert row[1] == username2
    assert row[2] == email2
    assert bcrypt.checkpw(password.encode(), bytes(row[3])) == True


def test_check_password(db_connection):
    username = "user1"
    password = "Password1!"
    assert UserController(db_connection)._check_password(username, password) == True

    password2 = "n0trightp@ssw0rd"
    assert UserController(db_connection)._check_password(username, password2) == False

    username2 = "user2"
    assert UserController(db_connection)._check_password(username2, password) == True


def test_change_password(db_connection):
    current_password2 = "Password1!"
    username2 = "user2"
    new_password2 = "Password2!"
    uc = UserController(db_connection)
    uc.change_password(username2, current_password2, new_password2)
    rows = db_connection.execute(
        """SELECT password FROM users WHERE username = %s""", [username2]
    )

    assert bcrypt.checkpw(new_password2.encode(), bytes(rows[0][0])) == True

    username1 = "user1"

    rows = db_connection.execute(
        """SELECT password FROM users WHERE username = %s""", [username1]
    )
    assert bcrypt.checkpw(current_password2.encode(), bytes(rows[0][0])) == True
    assert bcrypt.checkpw(new_password2.encode(), bytes(rows[0][0])) == False


def test_auth_user(db_connection):
    uc = UserController(db_connection)

    username = "user1"
    password = "Password1!"

    assert uc.auth_user(username, password) == {"user_id": 1, "username": username}

    username = "user2"
    assert uc.auth_user(username, password) == None


def test_delete_user(db_connection):
    uc = UserController(db_connection)

    uc.delete_account("user1")
    rows = db_connection.execute("""SELECT id FROM users""")
    assert len(rows) == 1
    assert len(rows[0]) == 1
    assert rows[0][0] == 2

    uc.delete_account("user2")
    rows = db_connection.execute("""SELECT id FROM users""")
    assert len(rows) == 0