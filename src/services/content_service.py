from os import getenv

from flask import render_template, session
from sqlalchemy import or_

from src import db
from src.models.models import Album, Artist, Genre, Link


class ContentService:

    @staticmethod
    def get_all_content(page):
        session["page"] = page
        session.modified = True
        rows_per_page = int(getenv("ROWS_PER_PAGE"))
        return Album.query.join(Artist, Album.artist_id == Artist.id) \
            .join(Genre, Album.genre_id == Genre.id) \
            .outerjoin(Link, or_(Link.album_id == Album.id, Link.album_id is None)) \
            .add_columns(Album.album_title, Album.id, Album.released_date,
                         Artist.artist_name, Genre.genre, Artist.id, Link) \
            .order_by(Artist.artist_name).paginate(page=page,
                                                   per_page=rows_per_page)

    @staticmethod
    def get_artist_content(artist_id):
        return Artist.query.join(Album, Album.artist_id == Artist.id) \
            .join(Genre, Album.genre_id == Genre.id) \
            .add_columns(Album.album_title, Album.released_date,
                         Artist.artist_name, Genre.genre).filter(Artist.id == artist_id).all()

    @staticmethod
    def get_content_by_release_year(year, page):
        rows_per_page = int(getenv("ROWS_PER_PAGE"))
        return Artist.query.join(Album, Album.artist_id == Artist.id) \
            .join(Genre, Album.genre_id == Genre.id) \
            .add_columns(Album.album_title, Album.released_date,
                         Artist.artist_name, Genre.genre) \
            .filter(Album.released_date == year).paginate(page=page,
                                                          per_page=rows_per_page)

    @staticmethod
    def get_content_by_genre(genre, page):
        rows_per_page = int(getenv("ROWS_PER_PAGE"))
        return Artist.query.join(Album, Album.artist_id == Artist.id) \
            .join(Genre, Genre.id == Album.genre_id) \
            .add_columns(Artist.artist_name, Album.album_title, Genre.genre, Album.released_date) \
            .filter(Genre.genre == genre) \
            .paginate(page=page,
                      per_page=rows_per_page)

    @staticmethod
    def search_content(form, page, rows_per_page):
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


