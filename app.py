from flask import Flask, request, render_template, session, redirect
from lib.db_connection import DatabaseConnection
from lib.user.user_controller import UserController
from lib.user.user import User
from lib.post.post_controller import PostController
import datetime, secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


@app.route("/", methods=["GET"])
def index():
    posts = PostController(DatabaseConnection()).get_published()
    return render_template("index.html", session=session, posts=posts)


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if "user_id" not in session:
        return redirect("/", 302)
    posts = PostController(DatabaseConnection()).get_posts(session["user_id"])
    return render_template("posts.html", posts=posts)


@app.route("/createpost", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/", 302)
    if request.method == "POST":
        title = request.form.get("post-title")
        body = request.form.get("post-body")
        if request.form.get("submit") == "Update":
            post_id = request.form.get("post-id")
            edited_at = str(datetime.datetime.now())
            post = PostController(DatabaseConnection()).update_post(
                post_id, session["user_id"], title, body, edited_at
            )
        else:
            created_at = str(datetime.datetime.now())
            post = PostController(DatabaseConnection()).add_post(
                session["user_id"], title, body, created_at
            )
        session["post_id"] = post.id
        return redirect("/view")
    return render_template("createpost.html")


@app.route("/view", methods=["GET", "POST"])
def view_post():
    if "post_id" not in session:
        post = PostController(DatabaseConnection()).get_one_post(
            request.form.get("post-id")
        )
    else:
        post = PostController(DatabaseConnection()).get_one_post(session["post_id"])
    return render_template("viewpost.html", post=post)


@app.route("/edit", methods=["GET", "POST"])
def edit_post():
    post_id = request.form.get("post-id")
    title = request.form.get("post-title")
    body = request.form.get("post-body")
    return render_template("edit.html", post_id=post_id, title=title, body=body)


@app.route("/publish", methods=["GET", "POST"])
def publish():
    if "user_id" not in session:
        return redirect("/", 302)
    if request.method == "POST":
        post_id = request.form.get("post-id")
        PostController(DatabaseConnection()).publish(post_id)
    return redirect("/posts")


@app.route("/delete", methods=["GET", "POST"])
def delete_post():
    if "user_id" in session:
        post_id = request.form.get("post-id")
        PostController(DatabaseConnection()).delete_one(post_id)
    return redirect("/posts")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect("/", 302)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        UserController(DatabaseConnection()).add_user(username, password, email)
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/", 302)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UserController(DatabaseConnection()).check_user(username, password)
        if user != None:
            session["username"] = user.username
            session["user_id"] = user.id
            return redirect("/")
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_id", default=None)
    session.pop("username", default=None)
    return redirect("/")


@app.route("/account", methods=["GET"])
def account():
    if "user_id" not in session:
        return redirect("/", 302)

    return render_template("account.html")


@app.route("/changepassword", methods=["POST"])
def change_password():
    current_password = request.form.get("currentpass")
    new_password = request.form.get("newpass")
    UserController(DatabaseConnection()).change_password(
        session["user_id"], current_password, new_password
    )
    return redirect("/account")


@app.route("/deleteaccount", methods=["POST"])
def deleteaccount():
    PostController(DatabaseConnection()).delete_all(session["user_id"])
    UserController(DatabaseConnection()).delete_account(session["username"])
    session.pop("user_id", default=None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
