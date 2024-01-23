from lib.post.post import Post
import re


class PostController:
    def __init__(self, connection):
        self._connection = connection

    def add_post(self, user_id, title, body, created_at, id):
        if self._check_title(title):
            if id == None:
                row = self._connection.execute(
                    """INSERT INTO posts (user_id, title, body, created_at, last_edited, published) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id""",
                    [
                        user_id,
                        title,
                        body,
                        created_at,
                        created_at,
                        False,
                    ],
                )
            else:
                rows = self._connection.execute(
                    """UPDATE posts SET title = %s, body = %s, last_edited = %s WHERE id = %s and user_id = %s RETURNING id""",
                    [title, body, created_at, id, user_id],
                )

                row = rows[0]
            post = self.get_one_post(row[0])
            return post

    def get_one_post(self, post_id):
        rows = self._connection.execute(
            """SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = %s""",
            [post_id],
        )
        if len(rows) == 1:
            row = rows[0]
            return Post(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def get_posts(self, user_id):
        rows = self._connection.execute(
            """SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id WHERE user_id = %s ORDER BY created_at DESC""",
            [user_id],
        )
        posts = []

        for row in rows:
            post = Post(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            posts.append(post)
        return posts

    def get_published(self):
        rows = self._connection.execute(
            """SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id WHERE published = True ORDER BY created_at DESC"""
        )
        posts = []

        for row in rows:
            post = Post(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            posts.append(post)
        return posts

    def publish(self, post_id):
        self._connection.execute(
            """UPDATE posts SET published = NOT published WHERE id = %s""", [post_id]
        )

    def delete_one(self, post_id):
        self._connection.execute("""DELETE FROM posts WHERE id=%s""", [post_id])

    def delete_all(self, user_id):
        self._connection.execute("""DELETE FROM posts WHERE user_id = %s""", [user_id])

    def _check_title(self, text):
        return True
        # if re.match(r"^[^';\r\n]*$", text):
        #     return True
        # return False
