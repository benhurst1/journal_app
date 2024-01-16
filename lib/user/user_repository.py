class UserRespository:
    def __init__(self, connection):
        self._connection = connection

    def add_user(self, user):
        self._connection.execute(
            """INSERT INTO users (username, email, password) VALUES (%s, %s, %s)""",
            [user.username, user.email, user.password],
        )

    def check_user(self, user):
        rows = self._connection.execute(
            """SELECT id, username, email FROM users WHERE username=%s AND password=%s""",
            [user.username, user.password],
        )
        print(rows)
        if len(rows) == 1:
            return rows[0]
        return None

    def change_password(self, user, new_password):
        self._connection.execute(
            """UPDATE users SET password = %s WHERE id = %s AND username = %s AND password = %s""",
            [new_password, user.id, user.username, user.password],
        )
