from flask import Flask, request, render_template, session, redirect
from lib.db_connection import DatabaseConnection
from lib.user.user_repository import UserRespository
from lib.user.user import User
from lib.post.post import Post
from lib.post.post_repository import PostRepository
import psycopg2
import datetime, secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


@app.route("/", methods=["GET"])
def index():
    posts = []
    for row in PostRepository(DatabaseConnection()).get_published():
        post = Post(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        posts.append(post)
    return render_template("index.html", session=session, posts=posts)


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if "user_id" not in session:
        return redirect("/", 302)
    posts = []
    for row in PostRepository(DatabaseConnection()).get_posts(session["user_id"]):
        post = Post(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        posts.append(post)
    return render_template("posts.html", posts=posts)


@app.route("/createpost", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/", 302)
    if request.method == "POST":
        title = request.form.get("post-title")
        body = request.form.get("post-body")
        created_at = str(datetime.datetime.now())
        post = Post(
            session["user_id"], title, body, created_at, created_at, False, None
        )
        PostRepository(DatabaseConnection()).add_post(post)
    return render_template("createpost.html")


@app.route("/publish", methods=["GET", "POST"])
def publish():
    if "user_id" not in session:
        return redirect("/", 302)
    if request.method == "POST":
        post_id = request.form.get("post-id")
        PostRepository(DatabaseConnection()).publish(post_id)
    return redirect("/posts")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect("/", 302)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User(username, password, email)
        UserRespository(DatabaseConnection()).add_user(user)
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/", 302)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username, password)
        user_id = UserRespository(DatabaseConnection()).check_user(user)
        if user_id != None:
            session["user_id"] = user_id
            return redirect("/")
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_id", default=None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
