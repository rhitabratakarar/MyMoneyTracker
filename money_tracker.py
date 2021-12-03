from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
from datetime import datetime


AUTH = "AUTH"
app = Flask(__name__)
DATABASE = "database.db"
app.secret_key = "rintu"


def check_database_existence():
    connection = sqlite3.connect(DATABASE)
    query = f"""create table if not exists {AUTH} (
                id integer primary key autoincrement,
                username varchar(255) not null unique,
                password varchar(255) not null
    )"""
    cursor = connection.cursor()

    # create the table if not exists.
    cursor.execute(query)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET"])
@app.route("/welcome", methods=["GET"])
def index():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        if session.get('username'):
            return redirect(url_for("logs"))

        # fetch posted form data.
        username = request.form.get("username")
        password = request.form.get("password")

        # check for the validity of the form data from database.
        connection = sqlite3.connect("database.db")
        query = f"select username, password from {AUTH} where username='{username}'"
        cursor = connection.cursor()

        cursor.execute(query)
        fetched_data = cursor.fetchone()
        connection.close()

        if not fetched_data:
            return "Username and Password combination do not match! <a href='/login'>Click here to login again</a>"

        u, p = fetched_data

        # send the user to logs page.
        if u == username and p == password:
            session["username"] = request.form.get("username")
            return redirect(url_for("logs"))
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        form_password = request.form.get("password")
        form_username = request.form.get("username")

        connection = sqlite3.connect(f"{DATABASE}")
        cursor = connection.cursor()

        # user creation query
        query = f"INSERT INTO {AUTH} (username, password) VALUES ('{form_username}', '{form_password}')"

        cursor.execute(query)

        # create a new table for the new user
        table_creation_query = f"""CREATE TABLE {form_username} (
            id integer primary key autoincrement,
            money integer,
            reason text,
            transaction_time timestamp
        )"""

        cursor.execute(table_creation_query)

        connection.commit()
        connection.close()

        # redirect the user to login
        return "You are signed up. <a href='/login'>click here to login</a>"
    else:
        return render_template("signup.html")


@app.route("/deposit", methods=["POST", "GET"])
def deposit():
    if not session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":

        # retrieve the form data
        amount = request.form.get("amount")
        reason = request.form.get("reason")

        # connect to the database
        connection = sqlite3.connect(f"{DATABASE}")
        cursor = connection.cursor()

        # calculate current date.
        date = datetime.now()

        query = f"""insert into {session.get('username')} ('money', 'reason', 'transaction_time')
        values (?,?,?);"""

        cursor.execute(query, (amount, reason, date))

        connection.commit()
        connection.close()

        return redirect(url_for("logs"))
    else:
        return render_template("deposit.html")


@app.route("/withdraw", methods=["POST", "GET"])
def withdraw():
    if not session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":
        amount = request.form.get("amount")
        reason = request.form.get("reason")

        if int(amount) > 0:
            amount = str(-int(amount))

        date = datetime.now()

        # connect to the database
        connection = sqlite3.connect(f"{DATABASE}")
        cursor = connection.cursor()

        query = f"""insert into {session.get('username')} ('money', 'reason', 'transaction_time')
        values (?,?,?);"""

        cursor.execute(query, (amount, reason, date))

        connection.commit()
        connection.close()

        return redirect(url_for("logs"))
    else:
        return render_template("withdraw.html")


@app.route("/logs", methods=["POST", "GET"])
def logs():
    if not session.get("username"):
        return redirect(url_for("index"))

    connection = sqlite3.connect(f"{DATABASE}")

    query = f"""select * from {session.get('username')}
            order by id desc;"""

    cursor = connection.cursor()

    cursor.execute(query)
    logs = cursor.fetchall()

    balance_fetching_query = f"select sum(money) from {session.get('username')}"

    cursor.execute(balance_fetching_query)
    balance = cursor.fetchone()

    connection.close()

    return render_template("logs.html", username=session.get("username"), logs = logs, balance=balance[0])


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if session.get("username"):
        session.pop("username")
    return redirect(url_for("index"))


if __name__ == "__main__":
    check_database_existence()
    app.run(debug=True)
