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
            """SELECT id FROM users WHERE username=%s AND password=%s""",
            [user.username, user.password],
        )
        if len(rows) == 1:
            return rows[0][0]
        return None
