from flask import Flask, request, render_template, session, redirect
from lib.db_connection import DatabaseConnection
from lib.user.user_controller import UserController
from lib.post.post_controller import PostController
import datetime, secrets, os


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

def connect_to_database():
    if request.headers.get("User-Agent") == "Playwright":
        print("testing")
        return DatabaseConnection(test_mode=True)
    print("not testing")
    return DatabaseConnection(test_mode=False)


@app.route("/", methods=["GET"])
def index():
    posts = PostController(connect_to_database()).get_published()
    return render_template("index.html", session=session, posts=posts)


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if "user_id" not in session:
        return redirect("/", 302)
    posts = PostController(connect_to_database()).get_posts(session["user_id"])
    return render_template("posts.html", posts=posts)


@app.route("/createpost", methods=["GET", "POST"])
def create_post():
    if "user_id" in session:
        if request.method == "GET":
            if "id" not in request.args:
                return render_template("createpost.html", post=None)
            else:
                post_id = request.args["id"]
                post = PostController(connect_to_database()).get_one_post(post_id)
                return render_template("createpost.html", post=post)
        if request.method == "POST":
            post_id = None
            if request.form.get("post-id") != "":
                post_id = request.form.get("post-id")
            title = request.form.get("post-title")
            body = request.form.get("post-body")
            created_at = str(datetime.datetime.now())
            post = PostController(connect_to_database()).add_post(
                session["user_id"], title, body, created_at, post_id
            )
            print(post)
            if post == False:
                return redirect("/createpost")
            return redirect(f"/view?id={post.id}")
    return redirect("/")


@app.route("/view", methods=["GET", "POST"])
def view_post():
    post_id = request.args["id"]
    post = PostController(connect_to_database()).get_one_post(post_id)
    if post.published == True or session["user_id"] == post.user_id:
        return render_template("viewpost.html", post=post)
    else:
        return redirect("/")


@app.route("/publish", methods=["GET", "POST"])
def publish():
    if "user_id" in session:
        post_id = request.args["id"]
        PostController(connect_to_database()).publish(post_id)
    return redirect("/posts")


@app.route("/delete", methods=["GET", "POST"])
def delete_post():
    if "user_id" in session:
        post_id = request.args["id"]
        PostController(connect_to_database()).delete_one(post_id)
    return redirect("/posts")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect("/", 302)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if (
            UserController(connect_to_database()).add_user(username, password, email)
            == True
        ):
            return redirect("/login")
        else:
            return render_template("signup.html", error=True)
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UserController(connect_to_database()).auth_user(username, password)
        print(user)
        if user != None:
            session["username"] = user["username"]
            session["user_id"] = user["user_id"]
            return redirect("/")
        else:
            return render_template("login.html", error=True)
    return render_template("login.html", error=False)


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
    UserController(connect_to_database()).change_password(
        session["username"], current_password, new_password
    )
    return redirect("/account")


@app.route("/deleteaccount", methods=["GET"])
def deleteaccount():
    PostController(connect_to_database()).delete_all(session["user_id"])
    UserController(connect_to_database()).delete_account(session["username"])
    session.pop("user_id", default=None)
    return redirect("/")


if __name__ == "__main__":
    if os.getenv("APP_ENV") == "PRODUCTION":
        app.run(port=5000, host="0.0.0.0")
    app.run(debug=True, port=5000)
