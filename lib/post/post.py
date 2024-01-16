class Post:
    def __init__(
        self,
        user_id: int,
        title,
        body,
        created_at,
        last_edited,
        published,
        post_id=None,
    ):
        self.post_id = post_id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.last_edited = last_edited
        self.published = published
