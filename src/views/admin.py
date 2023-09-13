from flask import Blueprint
from flask_login import login_required

from src.forms.forms import AddGenreForm, EditAlbumForm, LoginForm
from src.services.admin_service import AdminService

admin = Blueprint("admin", __name__)


@admin.route("/main/dude/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return AdminService.login(form)


@admin.route("/logout")
@login_required
def logout_page():
    return AdminService.logout()


@admin.route("/main/dude", methods=["GET", "POST"])
@login_required
def admin_page():
    form = EditAlbumForm()
    add_genre_form = AddGenreForm()
    return AdminService.admin_main(form, add_genre_form)


@admin.route("/edit/<int:album_id>", methods=["GET", "POST"])
@login_required
def edit(album_id):
    form = EditAlbumForm()
    return AdminService.edit_album(album_id, form)


@admin.route("/delete/album/<int:id>", methods=["GET", "POST"])
@login_required
def delete_album(id):
    return AdminService.delete_album(id)
