from music_base import app, db
from music_base.models import Album, Artist, Genre, User
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .forms import EditAlbumForm


@app.route("/")
@app.route("/home")
def home_page():
    content = Album.query.join(Artist, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.id, Album.released_date,
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


@app.route("/main/dude/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("admin_page"))
            else:
                flash("Dude, it's not correct password! Try again!", category="danger")
        else:
            flash("User doesn't exist.", category="danger")

    return render_template("login.html", user=current_user)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))


@app.route("/main/dude", methods=["GET", "POST"])
@login_required
def admin_page():
    genres = Genre.query.all()
    if request.method == "POST":
        artist_title = request.form.get("artist_title")
        album_title = request.form.get("album_title")
        genre_id = request.form.get("genre_select")
        album_link = request.form.get("album_link")
        print(artist_title)
        print(album_title)
        print(genre_id)
        print(album_link)

    return render_template("admin_page.html", genres=genres)


@app.route("/edit/<int:album_id>", methods=["GET", "POST"])
@login_required
def edit(album_id):
    form = EditAlbumForm()

    content = Album.query.join(Artist, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album, Artist, Genre).filter(Album.id == album_id).order_by(
        Artist.artist_name).first()

    if form.validate_on_submit():
        content.Artist.artist_name = form.artist_name.data
        content.Album.album_title = form.album_title.data
        content.Album.released_date = form.released_year.data
        content.Album.genre_id = request.form.get("genre")
        db.session.add(content.Album)
        db.session.add(content.Artist)
        db.session.commit()
        flash("Successfully update!", category="success")
        return redirect(url_for("home_page"))
    form.artist_name.data = content.Artist.artist_name
    form.album_title.data = content.Album.album_title
    form.released_year.data = content.Album.released_date
    form.genre.data = content.Album.genre_id
    return render_template("edit_album.html", content=content, form=form)
