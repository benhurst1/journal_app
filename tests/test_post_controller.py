from lib.db_connection import DatabaseConnection
import pytest, datetime
from lib.post.post_controller import PostController


@pytest.fixture(scope="session")
def db_connection():
    dbconn = DatabaseConnection(test_mode=True)
    dbconn.execute(open("seeds/test_setup.sql", "r").read())
    dbconn.execute(open("seeds/setup.sql", "r").read())
    yield dbconn


def test_add_post(db_connection):
    user_id = 1
    username = "user1"

    db_connection.execute(
        """INSERT INTO users (username, email, password) VALUES (%s, 'email@email.com', 'password')""",
        [username],
    )

    pc = PostController(db_connection)

    title = "title of post"
    body = "body of post"
    created_at = datetime.datetime.strptime(
        "2024-01-22 18:55:11.994218", "%Y-%m-%d %H:%M:%S.%f"
    )
    post_id = 1
    post = pc.add_post(user_id, title, body, created_at, None)
    assert post.id == post_id
    assert post.title == title
    assert post.body == body
    assert post.created_at == created_at
    assert post.last_edited == created_at
    assert post.user_id == user_id
    assert post.published == False
    assert post.username == username

    new_title = "new title of post"
    new_body = "new body of post"
    edited_at = datetime.datetime.strptime(
        "2025-03-10 19:03:36.994218", "%Y-%m-%d %H:%M:%S.%f"
    )
    post = pc.add_post(user_id, new_title, new_body, edited_at, 1)
    assert post.id == post_id
    assert post.title == new_title
    assert post.body == new_body
    assert post.created_at == created_at
    assert post.last_edited == edited_at
    assert post.user_id == user_id
    assert post.published == False
    assert post.username == username


def test_get_one_post(db_connection):
    pc = PostController(db_connection)
    post = pc.get_one_post(1)
    assert post.id == 1

    post = pc.get_one_post(2)
    assert post == None


def test_get_posts(db_connection):
    username = 'user2'
    db_connection.execute(
        """INSERT INTO users (username, email, password) VALUES (%s, 'email2@email.com', 'password')""",
        [username],
    )
    
    pc = PostController(db_connection)
    user_id = 2

    title = "title of post2"
    body = "body of post2"
    created_at = datetime.datetime.strptime(
        "2024-01-22 18:55:11.994218", "%Y-%m-%d %H:%M:%S.%f"
    )
    
    post = pc.add_post(user_id, title, body, created_at, None)

    posts = pc.get_posts(1)
    assert posts[0] != post
    assert posts[0].id == 1
    assert posts[0].user_id == 1

    posts = pc.get_posts(2)
    assert posts[0].title == title
    assert posts[0].id == 2
