import pytest
from app import app


@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_get_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_signup(client):
    response = client.get("/signup")
    assert response.status_code == 200


def test_get_login(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_get_createpost(client):
    response = client.get("/createpost")
    assert response.status_code == 200