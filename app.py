from flask import Flask, request, render_template, g, session, redirect


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def post_index():
    return render_template("index.html")


@app.route("/createpost", methods=["GET"])
def get_create_post():
    return render_template("createpost.html")


@app.route("/createpost", methods=["POST"])
def post_create_post():
    return render_template("createpost.html")


@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def post_signup():
    return render_template("signup.html")


@app.route("/login", methods=["GET"])
def get_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def post_login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
