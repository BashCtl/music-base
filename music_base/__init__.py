from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
app.config["SECRET_KEY"] = "ee1fa70e6c35461896c12a0572012c76"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from music_base import routers