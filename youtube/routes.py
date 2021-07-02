from flask import render_template, url_for, request, redirect, session, flash
from youtube import app, db, bcrypt
from youtube.models import *
import random
from datetime import datetime
from flask.json import jsonify


@app.route("/")
def home():
	video_list = Video.query.all()
	random.shuffle(video_list)
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
			session["user"] = existing_user.id

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
	video_id = request.args.get("video_id")
	video = Video.query.filter_by(id=video_id).first()

	recommended_videos = Video.query.all()
	recommended_videos.remove(video)

	return render_template('video.html', video=video, recommended=recommended_videos)
	

@app.route("/alter_like", methods=['POST'])
def alter_like():
	request_data = request.get_json()
	print("request data = ", request_data)
	# will require the user id
	# will require the video id
	# will require the actual value (like/dislike)
	video_id = request_data["video_id"]
	user_id = request_data["user_id"]
	value = request_data["value"]
	print("Values sent:")
	print("user_id: ", user_id)
	print("video_id: ", video_id)
	print("value: ", value)

	# getting user object
	user_instance = User.query.filter_by(id=user_id).first()
	print("User dislikes: ", user_instance.dislikes)
	print("User likes: ", user_instance.likes)

	if value == "like":
		# there are 3 scenarios:
		# 	1) user has already liked the video, need to remove from 'Likes' table --> return value = 100
		# 	2) user has not liked/disliked this video, need to add to 'Likes' table --> return value = 200
		# 	3) user has previously disliked this video, need to remove from 'dislikes' and add to 'likes' --> return value = 300

		# checking for scenario 1
		for like in user_instance.likes:
			if like.video_id == int(video_id):
				# removing from Likes table
				like_instance = Like.query.filter_by(user_id=user_id, video_id=video_id).first()
				db.session.delete(like_instance)
				db.session.commit()
				return jsonify({"status": 100})
		
		# checking for scenario 2
		found_dislike = False
		for dislike in user_instance.dislikes:
			if dislike.video_id == int(video_id):
				found_dislike = True
				break
		
		if found_dislike == False:
			print("running scenario 2")
			# adding to likes table
			new_like = Like(user_id=user_id, video_id=video_id)
			db.session.add(new_like)
			db.session.commit()
			return jsonify({"status": 200})

		# running scenario 3
		print("running scenario 3")
		# removing from dislikes table
		dislike_instance = Dislike.query.filter_by(user_id=user_id, video_id=video_id).first()
		db.session.delete(dislike_instance)

		# adding to likes table
		new_like = Like(user_id=user_id, video_id=video_id)
		db.session.add(new_like)

		db.session.commit()
			
		return jsonify({"status": 300})
	elif value == "dislike":
		# there are 3 scenarios:
		# 	1) user has already disliked the video, need to remove from 'Dislike' table --> return value = 400
		# 	2) user has not liked/disliked this video, need to add to 'Dislike' table --> return value = 500
		# 	3) user has previously liked this video, need to remove from 'likes' and add to 'dislikes' --> return value = 600

		# checking for scenario 1
		for dislike in user_instance.dislikes:
			if dislike.video_id == int(video_id):
				# removing from Likes table
				dislike_instance = Dislike.query.filter_by(user_id=user_id, video_id=video_id).first()
				db.session.delete(dislike_instance)
				db.session.commit()
				return jsonify({"status": 400})
		
		# checking for scenario 2
		found_like = False
		for like in user_instance.likes:
			if like.video_id == int(video_id):
				found_like = True
				break
		
		if found_like == False:
			print("running scenario 2")
			# adding to dislikes table
			new_disike = Dislike(user_id=user_id, video_id=video_id)
			db.session.add(new_disike)
			db.session.commit()
			return jsonify({"status": 500})

		# running scenario 3
		print("running scenario 3")
		# removing from likes table
		like_instance = Like.query.filter_by(user_id=user_id, video_id=video_id).first()
		db.session.delete(like_instance)

		# adding to dislikes table
		new_dislike = Dislike(user_id=user_id, video_id=video_id)
		db.session.add(new_dislike)

		db.session.commit()
			
		return jsonify({"status": 600})
	else:
		return jsonify({"error_message" : "invalid value sent. Can either be 'like' or 'dislike'"})
