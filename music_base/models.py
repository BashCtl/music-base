from music_base import db
from music_base import bcrypt


class Genre(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    genre = db.Column(db.String(length=255), nullable=False, unique=True)


class Artist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    artist_name = db.Column(db.String(length=255), nullable=False, unique=True)


class Album(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    album_title = db.Column(db.String(length=255), nullable=False)
    released_date = db.Column(db.String(length=4), nullable=False)
    artist_id = db.Column(db.Integer(), db.ForeignKey("artist.id"), nullable=False)
    genre_id = db.Column(db.Integer(), db.ForeignKey("genre.id"), nullable=False)
    artist = db.relationship("Artist", backref="album")
    genre = db.relationship("Genre", backref="album")
