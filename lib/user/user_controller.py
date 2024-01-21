from lib.user.user import User
import bcrypt


class UserController:
    def __init__(self, connection):
        self._connection = connection

    def add_user(self, username, password, email):
        hashed = self._hash_password(password)
        rows = self._connection.execute(
            """INSERT INTO users (username, email, password) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING RETURNING id """,
            [username, email, hashed],
        )
        if len(rows) == 1:
            return True
        return False

    def auth_user(self, username, password):
        if self._check_password(username, password):
            rows = self._connection.execute(
                """SELECT id, username, password, email FROM users WHERE username=%s""",
                [username],
            )
            if len(rows) == 1:
                user = User(rows[0][0], rows[0][1], rows[0][2], rows[0][3])
                return user
        return None

    def change_password(self, username, password, new_password):
        if self._check_password(username, password):
            new_hashed = self._hash_password(new_password)
            self._connection.execute(
                """UPDATE users SET password = %s WHERE username = %s""",
                [new_hashed, username],
            )

    def delete_account(self, username):
        self._connection.execute(
            """DELETE FROM users WHERE username = %s""", [username]
        )

    def _hash_password(self, password):
        salt = bcrypt.gensalt(14)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def _check_password(self, username, input_password):
        hashed_password = self._get_hashed_password(username)
        if hashed_password == False:
            return False
        if bcrypt.checkpw(input_password.encode(), bytes(hashed_password)):
            return True
        return False

    def _get_hashed_password(self, username):
        hashed = self._connection.execute(
            """SELECT password FROM users WHERE username=%s""",
            [username],
        )
        if len(hashed[0]) == 1:
            return bytes(hashed[0][0])
        return False
