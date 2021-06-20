from flask import render_template, url_for, request, redirect, session, flash
from youtube import app, db, bcrypt
from youtube.models import *
import random
from datetime import datetime


@app.route("/")
def home():
	video_list = Video.query.all()
	random.shuffle(video_list)
	print(video_list)
	return render_template("home.html", videos=video_list, todays_date = datetime.utcnow())


@app.route("/login", methods=["GET", "POST"])
def login():
	if 'logged_in' in session:
		return redirect(url_for("home"))

	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		existing_user = User.query.filter_by(email=email).first()
		if existing_user is None:
			flash("Incorrect Email Entered", "error")
			return render_template("login.html")
		
		if bcrypt.check_password_hash(existing_user.password, password) == True:
			session["logged_in"] = True
			session["user"] = existing_user

			return redirect(url_for("home"))
		else:
			flash("Incorrect Password Entered", "error")
			return render_template("login.html")
	else:
		return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if 'logged_in' in session:
		return redirect(url_for("home"))

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


@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	session.pop('user', None)

	return redirect(url_for("login"))


@app.route('/video')
def video():
	video = Video.query.first()
	recommended_videos = Video.query.all()
	recommended_videos.remove(video)
	print(recommended_videos)
	return render_template('video.html', video=video, recommended=recommended_videos)