from music_base import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Genre(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    genre = db.Column(db.String(length=255), nullable=False, unique=True)


class Artist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    artist_name = db.Column(db.String(length=255), nullable=False, unique=True)


class Link(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    link = db.Column(db.String(length=255))
    album_id = db.Column(db.Integer(), db.ForeignKey("album.id"), nullable=False)
    album = db.relationship("Album", backref="link")


class Album(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    album_title = db.Column(db.String(length=255), nullable=False)
    released_date = db.Column(db.String(length=4), nullable=False)
    artist_id = db.Column(db.Integer(), db.ForeignKey("artist.id"), nullable=False)
    genre_id = db.Column(db.Integer(), db.ForeignKey("genre.id"), nullable=False)
    artist = db.relationship("Artist", backref="album")
    genre = db.relationship("Genre", backref="album")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=150), unique=True)
    password = db.Column(db.String(length=150))
