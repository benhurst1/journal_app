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
            """SELECT * FROM posts WHERE user_id = %s ORDER BY created_at DESC""",
            [user_id],
        )
        return posts

    def get_published(self):
        posts = self._connection.execute(
            """SELECT * FROM posts WHERE published = True ORDER BY created_at DESC"""
        )
        return posts

    def publish(self, post_id):
        self._connection.execute(
            """UPDATE posts SET published = NOT published WHERE id = %s""", [post_id]
        )

    def delete_all(self, user_id):
        self._connection.execute("""DELETE FROM posts WHERE user_id = %s""", [user_id])
