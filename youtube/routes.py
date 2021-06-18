# TODO: Use Sessions to keep user logged in

from flask import render_template, url_for, request, redirect, session, flash
from youtube import app, db, bcrypt
from youtube.models import *


@app.route("/")
def home():
	return "Hello World"


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		existing_user = User.query.filter_by(email=email).first()
		if existing_user is None:
			flash("Incorrect Email Entered", "error")
			return render_template("login.html")
		
		if bcrypt.check_password_hash(existing_user.password, password) == True:
			return redirect(url_for("home"))
		else:
			flash("Incorrect Password Entered", "error")
			return render_template("login.html")
	else:
		return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]
		username = request.form["username"]

		existing_username = User.query.filter_by(user_name=username).first()
		if existing_username is not None:
			flash("Username Already Taken", "error")
			return render_template("register.html")
		
		existing_email = User.query.filter_by(email=email).first()
		if existing_email is not None:
			flash("Email Already Taken", "error")
			return render_template("register.html")

		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		new_user = User(user_name=username, email=email, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash("Account Successfully Created", "success")
		return redirect(url_for("login"))
	else:
		return render_template("register.html")