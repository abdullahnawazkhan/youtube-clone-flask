from youtube import db
from datetime import datetime


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	user_name = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	videos = db.relationship('Video', backref='user', lazy=True)
	likes = db.relationship('Like', backref='user', lazy=True)
	dislikes = db.relationship('Dislike', backref='user', lazy=True)
	comments = db.relationship('Comment', backref='user', lazy=True)

	def __repr__(self):
		return f'{self.id}'


class Video(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60), nullable=False)
	description = db.Column(db.Text, nullable=True)
	date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)
	video_path = db.Column(db.Text, nullable=False)
	image_path = db.Column(db.Text, nullable=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	likes = db.relationship('Like', backref='video', lazy=True)
	dislikes = db.relationship('Dislike', backref='video', lazy=True)
	comments = db.relationship('Comment', backref='video', lazy=True)

	def __repr__(self):
		return f'{self.id}'


class Like(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)

	def __repr__(self):
		return f'{self.video_id}'


class Dislike(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)

	def __repr__(self):
		return f'{self.video_id}'


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)

	def __repr__(self):
		return f'{self.video_id}'