from music_base import app, db
from music_base.models import Album, Artist, Genre
from flask import render_template, jsonify


@app.route("/")
@app.route("/home")
def home_page():
    content = Album.query.join(Artist, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.released_date,
                     Artist.artist_name, Genre.genre, Artist.id).order_by(Artist.artist_name).all()
    return render_template("home.html", content=content)


@app.route("/artist/<id>")
def artist_page(id):
    artist_content = Artist.query.join(Album, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.released_date,
                     Artist.artist_name, Genre.genre).filter(Artist.id == id).all()
    if artist_content:
        return render_template("artist_page.html", artist_content=artist_content)
    return render_template("404.html")


@app.route("/albums/<year>")
def years_page(year):
    release_content = Artist.query.join(Album, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.released_date,
                     Artist.artist_name, Genre.genre).filter(Album.released_date == year).all()
    return render_template("release_page.html", release_content=release_content)


