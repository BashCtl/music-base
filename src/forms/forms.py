from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length
from src.models.models import Genre
from flask import current_app


def genre_choices():
    with current_app.app_context():
        return [(g.id, g.genre) for g in Genre.query.all()]


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditAlbumForm(FlaskForm):
    artist_name = StringField("Artist:", validators=[DataRequired()])
    album_title = StringField("Album title:", validators=[DataRequired()])
    released_year = StringField("Release Year:", validators=[DataRequired(), Length(4)])
    album_link = StringField("Album Link")
    genre = SelectField("Select genre: ", choices=genre_choices, coerce=int)
    submit = SubmitField("Save")


class AddGenreForm(FlaskForm):
    genre = StringField("New Genre:", validators=[DataRequired()])
    add_btn = SubmitField("Add")

class DeleteGenreForm(FlaskForm):
    genre = SelectField("Select genre: ", validators=[DataRequired()], choices=genre_choices, coerce=int)
    delete_btn = SubmitField("Delete")


class SearchForm(FlaskForm):
    searched = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")