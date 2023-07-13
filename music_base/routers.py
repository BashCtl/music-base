from music_base import app, db
from music_base.models import Album, Artist, Genre, User
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .forms import EditAlbumForm, AddGenre
from os import  getenv

@app.route("/")
@app.route("/home")
def home_page():
    page = request.args.get("page", 1, type=int)
    rows_per_page = int(getenv("ROWS_PER_PAGE"))
    content = Album.query.join(Artist, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.id, Album.released_date,
                     Artist.artist_name, Genre.genre, Artist.id).order_by(Artist.artist_name).paginate(page=page,per_page=rows_per_page)
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
    form = EditAlbumForm()
    add_genre_form = AddGenre()
    if form.submit.data and form.validate_on_submit():
        artist_name = form.artist_name.data
        album_title = form.album_title.data
        released_year = form.released_year.data
        genre_id = request.form.get("genre")
        if Album.query.filter_by(album_title=album_title).first():
            flash("Album already exists in database.", category="danger")
            return redirect(url_for("admin_page"))
        artist = Artist.query.filter_by(artist_name=artist_name).first()
        if artist is None:
            artist = Artist(artist_name=artist_name)
            db.session.add(artist)
        db.session.flush()
        album = Album(album_title=album_title, released_date=released_year,
                      artist_id=artist.id, genre_id=genre_id)
        db.session.add(album)
        db.session.commit()
        flash("Successfully added new album.", category="success")

        return redirect(url_for("admin_page"))

    if add_genre_form.add_btn.data and request.method == "POST":
        genre_name = add_genre_form.genre.data
        if Genre.query.filter_by(genre=genre_name).first():
            flash(f"{genre_name} - genre already exists in database.", category="danger")
        else:
            db.session.add(Genre(genre=genre_name))
            db.session.commit()
            flash(f"{genre_name} - genre successfully added.", category="success")
            return redirect(url_for("admin_page"))

    return render_template("admin_page.html", form=form, add_genre_form=add_genre_form)


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
