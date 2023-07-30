from src import app, db
from src.models.models import Album, Artist, Genre, Link
from src.forms.forms import SearchForm
from flask import render_template, request, Blueprint, session
from sqlalchemy import or_
from os import getenv

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home_page():
    page = request.args.get("page", 1, type=int)
    session["page"] = page
    session.modified = True
    rows_per_page = int(getenv("ROWS_PER_PAGE"))
    pagination = Album.query.join(Artist, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .outerjoin(Link, or_(Link.album_id == Album.id, Link.album_id is None)) \
        .add_columns(Album.album_title, Album.id, Album.released_date,
                     Artist.artist_name, Genre.genre, Artist.id, Link) \
        .order_by(Artist.artist_name).paginate(page=page,
                                               per_page=rows_per_page)

    return render_template("home.html", content=pagination)


@main.route("/artist/<int:id>")
def artist_page(id):
    artist_content = Artist.query.join(Album, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.released_date,
                     Artist.artist_name, Genre.genre).filter(Artist.id == id).all()
    if artist_content:
        return render_template("artist_page.html", artist_content=artist_content)
    return render_template("404.html")


@main.route("/albums/<year>")
def release_page(year):
    page = request.args.get("page", 1, int)
    rows_per_page = int(getenv("ROWS_PER_PAGE"))
    release_content = Artist.query.join(Album, Album.artist_id == Artist.id) \
        .join(Genre, Album.genre_id == Genre.id) \
        .add_columns(Album.album_title, Album.released_date,
                     Artist.artist_name, Genre.genre) \
        .filter(Album.released_date == year).paginate(page=page,
                                                      per_page=rows_per_page)
    return render_template("release_page.html", release_content=release_content, year=year)


@main.route("/genre/<string:type>")
def genre_page(type):
    page = request.args.get("page", 1, type=int)
    rows_per_page = int(getenv("ROWS_PER_PAGE"))
    content = Artist.query.join(Album, Album.artist_id == Artist.id) \
        .join(Genre, Genre.id == Album.genre_id) \
        .add_columns(Artist.artist_name, Album.album_title, Genre.genre, Album.released_date) \
        .filter(Genre.genre == type) \
        .paginate(page=page,
                  per_page=rows_per_page)

    return render_template("genre_page.html", content=content, genre=type)


# Pass Stuff to Navbar
@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route("/search", methods=["POST", "GET"])
def search():
    page = request.args.get("page", 1, type=int)
    rows_per_page = int(getenv("ROWS_PER_PAGE"))
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        session["searched"] = searched
        session.modified = True
        content = (db.session.query(Album, Artist, Genre)
                   .join(Artist, Artist.id == Album.artist_id)
                   .join(Genre, Genre.id == Album.genre_id)
                   .filter(or_(Album.album_title.like(f"%{searched}%"),
                               Artist.artist_name.like(f"%{searched}%"),
                               Genre.genre.like(f"%{searched}%")))
                   .paginate(page=page, per_page=rows_per_page))
        return render_template("search.html", form=form, searched=searched, content=content)
    content = (db.session.query(Album, Artist, Genre)
               .join(Artist, Artist.id == Album.artist_id)
               .join(Genre, Genre.id == Album.genre_id)
               .filter(or_(Album.album_title.like(f"%{session['searched']}%"),
                           Artist.artist_name.like(f"%{session['searched']}%"),
                           Genre.genre.like(f"%{session['searched']}%")))
               .paginate(page=page, per_page=rows_per_page))
    return render_template("search.html", form=form, content=content)
