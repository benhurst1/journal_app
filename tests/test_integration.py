from lib.db_connection import DatabaseConnection
import pytest
from playwright.sync_api import Page, sync_playwright
import time


@pytest.fixture(scope="session")
def db_connection():
    dbconn = DatabaseConnection(test_mode=True)
    dbconn.execute(open("seeds/test_setup.sql", "r").read())
    dbconn.execute(open("seeds/setup.sql", "r").read())
    yield dbconn


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent="Playwright")
        page = context.new_page()
        yield page
        browser.close()


def test_flask_app(page, db_connection):
    page.goto("http://127.0.0.1:5000/signup")
    page.get_by_placeholder("Enter username").click()
    page.get_by_placeholder("Enter username").fill("user1")
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill("email2@email.com")
    page.get_by_placeholder("Enter email").press("Tab")
    page.get_by_placeholder("Enter password").fill("Password93!")
    page.get_by_role("button", name="Create").click()
