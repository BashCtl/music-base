from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from src import db
from src.models.models import User, Album, Artist, Genre, Link
from src.forms.forms import AddGenreForm, EditAlbumForm, LoginForm


class AdminService:

    @staticmethod
    def login(form: LoginForm):
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("admin.admin_page"))
                else:
                    flash("Dude, it's not correct password! Try again!", category="danger")
            else:
                flash("User doesn't exist.", category="danger")

        return render_template("login.html", user=current_user, form=form)

    @staticmethod
    def admin_main(form: EditAlbumForm, add_genre_form: AddGenreForm):
        AdminService.__add_album(form)
        AdminService.__add_genre(add_genre_form)

        return render_template("admin_page.html", form=form, add_genre_form=add_genre_form)

    @staticmethod
    def edit_album(album_id, form: EditAlbumForm):
        album_content = Album.query.join(Artist, Album.artist_id == Artist.id) \
            .join(Genre, Album.genre_id == Genre.id) \
            .add_columns(Artist, Genre).filter(Album.id == album_id).order_by(
            Artist.artist_name).first()

        link = Link.query.filter_by(album_id=album_content.Album.id).first()

        if form.validate_on_submit():
            album_content.Artist.artist_name = form.artist_name.data
            album_content.Album.album_title = form.album_title.data
            album_content.Album.released_date = form.released_year.data
            album_content.Album.genre_id = request.form.get("genre")
            link = Link(link=form.album_link.data, album_id=album_content.Album.id)
            if not link:
                db.session.add(link)
            db.session.commit()
            flash("Successfully update!", category="success")
            return redirect(url_for("main.home_page", page=session["page"]))
        form.artist_name.data = album_content.Artist.artist_name
        form.album_title.data = album_content.Album.album_title
        form.released_year.data = album_content.Album.released_date
        form.genre.data = album_content.Album.genre_id
        if link:
            form.album_link.data = link.link

        return render_template("edit_album.html", form=form)

    @staticmethod
    def delete_album(id):
        album = Album.query.get_or_404(id)
        if album:
            db.session.delete(album)
            db.session.commit()
            flash(f"{album.album_title} - was deleted", category="info")
        return redirect(url_for("main.home_page", page=session["page"]))

    @staticmethod
    def logout():
        logout_user()
        flash("You have been logged out!", category="info")
        return redirect(url_for("main.home_page"))

    @staticmethod
    def __add_album(form: EditAlbumForm):
        if form.submit.data and form.validate_on_submit():
            artist_name = form.artist_name.data
            album_title = form.album_title.data
            released_year = form.released_year.data
            genre_id = request.form.get("genre")
            album_link = form.album_link.data
            if Album.query.filter_by(album_title=album_title).first():
                flash("Album already exists in database.", category="danger")
                return redirect(url_for("admin.admin_page"))
            artist = Artist.query.filter_by(artist_name=artist_name).first()
            if artist is None:
                artist = Artist(artist_name=artist_name)
                db.session.add(artist)
            db.session.flush()
            album = Album(album_title=album_title, released_date=released_year,
                          artist_id=artist.id, genre_id=genre_id)
            db.session.add(album)
            db.session.flush()
            if album_link:
                link = Link(link=album_link, album_id=album.id)
                db.session.add(link)
            db.session.commit()
            flash("Successfully added new album.", category="success")

            return redirect(url_for("admin.admin_page"))

    @staticmethod
    def __add_genre(add_genre_form: AddGenreForm):
        if add_genre_form.add_btn.data and request.method == "POST":
            genre_name = add_genre_form.genre.data
            if Genre.query.filter_by(genre=genre_name).first():
                flash(f"{genre_name} - genre already exists in database.", category="danger")
            else:
                db.session.add(Genre(genre=genre_name))
                db.session.commit()
                flash(f"{genre_name} - genre successfully added.", category="success")
                return redirect(url_for("admin.admin_page"))
