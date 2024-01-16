class PostRepository:
    def __init__(self, connection):
        self._connection = connection

    def add_post(self, post):
        self._connection.execute(
            """INSERT INTO posts (user_id, title, body, created_at, last_edited, published) VALUES(%s, %s, %s, %s, %s, %s)""",
            [
                post.user_id,
                post.title,
                post.body,
                post.created_at,
                post.last_edited,
                False,
            ],
        )

    def get_posts(self, user_id):
        posts = self._connection.execute(
            """SELECT * FROM posts WHERE user_id = %s""", [user_id]
        )
        return posts

    def get_published(self):
        posts = self._connection.execute(
            """SELECT * FROM posts WHERE published = True"""
        )
        return posts

    def publish(self, post_id):
        self._connection.execute(
            """UPDATE posts SET published = True WHERE id = %s""", [post_id]
        )
