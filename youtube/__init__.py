from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from flask_bcrypt import Bcrypt

app = Flask(__name__)

from youtube import routes