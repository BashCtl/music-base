import csv
from src.models.models import db, Album, Artist, Genre, User
from src import app


def get_albums(file_csv):
    with open(file_csv, mode="r") as file:
        reader = csv.DictReader(file)
        albums = {row["Album"] for row in reader}
        return albums


def write_album_and_id_to_csv(output_file):
    with app.app_context():
        content = Album.query.all()
        with open(output_file, "w") as file:
            header = ["album_id", "album_title"]
            writer = csv.writer(file)
            writer.writerow(header)
            for album in content:
                writer.writerow([album.id, album.album_title])


# get_albums("albumlist.csv")

write_album_and_id_to_csv("id_and_albums.csv")
