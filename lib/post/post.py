class Post:
    def __init__(
        self, id, user_id: int, title, body, created_at, last_edited, published, username
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.last_edited = last_edited
        self.published = published
        self.username = username
