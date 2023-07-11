from music_base.models import db, Album, Artist, Genre, User, Role
from music_base import app
from werkzeug.security import generate_password_hash
import csv


def read_csv(file):
    with open(file, mode="r") as file:
        csv_file = csv.reader(file)
        next(csv_file, None)
        return list(csv_file)


def populate_users_db(data):
    for user in data:
        username = user[0]
        password = user[1]
        role_id = user[2]
        user = User(username=username, password=generate_password_hash(password), role_id=role_id)
        try:
            with app.app_context():
                db.create_all()
                db.session.add(user)
                db.session.commit()
        except Exception as err:
            print(f"Something went wrong:\n {err}")


def create_role_table():
    with app.app_context():
        db.create_all()
        Role.insert_roles()
        print("Role was inserted")


def populate_genre_db(data):
    for line in data:
        genre_type = line[4]
        print(genre_type)
        try:
            db_genre = Genre(genre=genre_type)
            with app.app_context():
                db.create_all()
                db.session.add(db_genre)
                db.session.commit()
        except Exception:
            print("Something went wrong.")


def populate_artist_db(data):
    artists = {line[3].strip() for line in data}
    for artist_name in artists:
        try:
            with app.app_context():
                artist = Artist(artist_name=artist_name)
                db.session.add(artist)
                db.session.commit()
                print("Committed to DB")
        except Exception:
            print(f"'{artist_name}' - artists already added.")


def populate_album_db(data):
    for line in data:
        album_title = line[2]
        released_date = line[1]
        artist_name = line[3]
        genre = line[4]
        try:
            with app.app_context():
                genre_id = Genre.query.filter_by(genre=genre).first().id
                artist_id = Artist.query.filter_by(artist_name=artist_name).first().id
                album = Album(album_title=album_title, released_date=released_date, genre_id=genre_id,
                              artist_id=artist_id)
                db.session.add(album)
                db.session.commit()
        except:
            print("Something went wrong.")


data_file = read_csv("albumlist.csv")

# populate_genre_db(data_file)
# populate_artist_db(data_file)
# populate_album_db(data_file)
# create_role_table()
users_data = read_csv("users.csv")
populate_users_db(users_data)
