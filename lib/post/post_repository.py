class PostRepository:
    def __init__(self, connection):
        self._connection = connection

    def add_post(self, post):
        self._connection.execute(
            """INSERT INTO posts (user_id, title, body, created_at, last_edited) VALUES(%s, %s, %s, %s, %s)""",
            [post.user_id, post.title, post.body, post.created_at, post.last_edited],
        )