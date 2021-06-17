from flask import render_template, url_for, request, redirect, session, flash
from youtube import app


@app.route("/")
def home():
	return "Hello World"