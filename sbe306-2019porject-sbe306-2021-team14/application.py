import os
from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
import mysql.connector
from mysql.connector import errorcode



app = Flask(__name__)
 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
 
#set db as global variable
db = ""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="NEONATAL"
)
db = mydb.cursor()

def check_logged_in():
    db.execute("SELECT * FROM users WHERE username = :username AND password = :password LIMIT 1",
               username = session.get("username"),password = session.get("password"))
    data = db.fetchone()
    if data is not None:
        return render_template("home.html")
    return True

@app.route("/", methods = ["GET", "POST"])
def index():
	#check_logged_in()
	if request.method == "GET":
		return render_template("index.html")
	elif request.method == "POST":
		uname = request.form.get("usr")
		password = request.form.get("pss")

		print(uname, " ", password, "\n")
		db.execute("SELECT * FROM users")
		data = db.fetchone()
		print(data)
		if data[5] != password:
			return render_template("signup.html")
		else:
			return redirect("/")





@app.route("/signup", methods = ["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template("signup.html")
	elif request.method == "POST":
		Fname = request.form.get("qwe")
		Lname = request.form.get("asd")
		username = request.form.get("zxc")
		email = request.form.get("rty")
		password = request.form.get("fgh")
		print(Fname)
		print(Lname)
		print(username)
		sql = "INSERT INTO users (ID, firstname,lastname, username, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
		val = (5, Fname, Lname, username, email, password)
		db.execute(sql, val)
		mydb.commit()  
		return render_template("signup.html")

@app.route("/contact-form", methods = ["GET", "POST"])
def contact_form():
	if request.method == "GET":
		return render_template("contact-form.html")
	msg = request.form.get("message")
	return render_template("thankyou.html", "contacting us!")


if __name__ == "__main__":
	app.run(debug = True)