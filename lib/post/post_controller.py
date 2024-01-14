from lib.post.post import Post


class PostController:
    def create_post_object(self, user_id, title, body, created_at, last_edited):
        post = Post(user_id, title, body, created_at, last_edited)
        return post
