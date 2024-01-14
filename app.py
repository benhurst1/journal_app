from flask import Flask, request, render_template, g, session, redirect
from lib.db_connection import DatabaseConnection
from lib.user.user_repository import UserRespository
from lib.user.user_controller import UserController
import psycopg2

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def post_index():
    return render_template("index.html")


@app.route("/createpost", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        pass
    return render_template("createpost.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        user = UserController().create_user_object(username, email, password)
        conn = DatabaseConnection()
        user_repo = UserRespository(conn)
        user_repo.add_user(user)
    return render_template("signup.html")


@app.route("/login", methods=["GET"])
def get_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def post_login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
