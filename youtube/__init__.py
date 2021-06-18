from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from youtube import routes, models