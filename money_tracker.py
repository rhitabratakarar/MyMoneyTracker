from flask import Flask, request, render_template, session

app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/welcome", methods=["GET"])
def index_page():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return "This is the signup page."


@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    return "This is the deposit page."


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    return "This is the withdraw page."


@app.route("/logs", methods=["GET", "POST"])
def logs():
    return "LOGS will be present here."


if __name__ == "__main__":
    app.run(debug=True)
