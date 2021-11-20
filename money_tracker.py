from flask import Flask, request, render_template, session
import sqlite3


AUTH = "AUTH"
app = Flask(__name__)
DATABASE = "database.db"


def check_database_existence():
    connection = sqlite3.connect(DATABASE)
    query = f"""create table if not exists {AUTH} (
                id integer primary key autoincrement,
                email varchar(255) not null unique,
                password varchar(255) not null
    )"""
    cursor = connection.cursor()

    # create the table if not exists.
    cursor.execute(query)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET"])
@app.route("/welcome", methods=["GET"])
def index_page():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # fetch posted form data.
        email = request.form.get("email")
        password = request.form.get("password")

        # check for the validity of the form data from database.
        connection = sqlite3.connect("database.db")
        query = ""
        cursor = connection.cursor()

        if query != "":
            cursor.execute(query)

        connection.close()

    else:
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
    check_database_existence()
    app.run(debug=True)
