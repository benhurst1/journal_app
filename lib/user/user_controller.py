from lib.user.user import User


class UserController:
    def __init__(self, connection):
        self._connection = connection

    def add_user(self, username, password, email):
        self._connection.execute(
            """INSERT INTO users (username, email, password) VALUES (%s, %s, %s)""",
            [username, email, password],
        )

    def check_user(self, username, password):
        rows = self._connection.execute(
            """SELECT id, username, password, email FROM users WHERE username=%s AND password=%s""",
            [username, password],
        )
        if len(rows) == 1:
            user = User(rows[0][0], rows[0][1], rows[0][2], rows[0][3])
            return user
        return None

    def change_password(self, user_id, password, new_password):
        self._connection.execute(
            """UPDATE users SET password = %s WHERE user_id = %s AND password = %s""",
            [new_password, user_id, password],
        )

    def delete_account(self, username):
        self._connection.execute(
            """DELETE FROM users WHERE username = %s""", [username]
        )
