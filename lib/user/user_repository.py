class UserRespository:
    def __init__(self, connection):
        self._connection = connection

    def add_user(self, user):
        self._connection.execute(
            """INSERT INTO users (username, email, password) VALUES (%s, %s, %s)""",
            [user.username, user.email, user.password],
        )
