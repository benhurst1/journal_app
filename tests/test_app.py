import pytest
from playwright.sync_api import sync_playwright
from app import app
from seeds.setup import *
from lib.db_connection import DatabaseConnection


@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


# @pytest.fixture(scope="function")
# def browser():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         yield browser


# @pytest.fixture()
# def db_connection():
#     conn = DatabaseConnection()
#     conn.connect()
#     conn.execute("TRUNCATE posts CASCADE")
#     conn.execute("TRUNCATE users CASCADE")
#     yield conn


def test_routes(client):
    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/signup")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200
    response = client.get("/createpost")
    assert response.status_code == 200


# def test_signup(browser, db_connection):
#     conn = db_connection
#     page = browser.new_page()
#     page.goto("http://localhost:5000/signup")
#     page.fill("input[name=username]", " benhurst")
#     page.fill("input[name=email]", "email@email.com")
#     page.fill("input[name=password]", "password")
#     page.click("text=Create")
#     p_tag = page.locator("p")
#     assert list(conn.execute("SELECT * FROM users")) == "Hello!"
