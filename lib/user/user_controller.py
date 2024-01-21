import bcrypt, re


class UserController:
    def __init__(self, connection):
        self._connection = connection
        self.deny = """ ?<>!@#$%^&*()'[]\{\}\\`~+=|"""

    def add_user(self, username, password, email):
        if self._check_username(username) and self._check_password_min_req(password):
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
                return {"username": rows[0][0], "user_id": rows[0][1]}
        return None

    def change_password(self, username, password, new_password):
        if self._check_password(username, password) and self._check_password_min_req(
            new_password
        ):
            new_hashed = self._hash_password(new_password)
            self._connection.execute(
                """UPDATE users SET password = %s WHERE username = %s""",
                [new_hashed, username],
            )

    def delete_account(self, username):
        self._connection.execute(
            """DELETE FROM users WHERE username = %s""", [username]
        )

    def _check_username(self, username):
        if re.match(r"^[A-Za-z0-9_]+$", username):
            return True
        return False

    def _check_password_min_req(self, input_password):
        if re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            input_password,
        ):
            return True
        return False

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
