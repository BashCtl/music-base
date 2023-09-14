from os import getenv

from flask import render_template, request, Blueprint

from src.forms.forms import SearchForm
from src.services.content_service import ContentService

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home_page():
    page = request.args.get("page", 1, type=int)
    pagination = ContentService.get_all_content(page)
    return render_template("home.html", content=pagination)


@main.route("/artist/<int:id>")
def artist_page(id):
    artist_content = ContentService.get_artist_content(id)
    if artist_content:
        return render_template("artist_page.html", artist_content=artist_content)
    return render_template("404.html")


@main.route("/albums/<year>")
def release_page(year):
    page = request.args.get("page", 1, int)
    release_content = ContentService.get_content_by_release_year(year, page)
    return render_template("release_page.html", release_content=release_content, year=year)


@main.route("/genre/<string:type>")
def genre_page(type):
    page = request.args.get("page", 1, type=int)
    content = ContentService.get_content_by_genre(type, page)
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
    return ContentService.search_content(form, page, rows_per_page)
