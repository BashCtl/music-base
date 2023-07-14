from music_base import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Permission:
    ADMIN = 16
    COMMENT = 2


class Genre(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    genre = db.Column(db.String(length=255), nullable=False, unique=True)


class Artist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    artist_name = db.Column(db.String(length=255), nullable=False, unique=True)

    def __repr__(self):
        return f"Artist({self.id}, {self.artist_name})"


class Link(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    link = db.Column(db.String(length=255))
    album_id = db.Column(db.Integer(), db.ForeignKey("album.id"), nullable=False)


class Album(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    album_title = db.Column(db.String(length=255), nullable=False)
    released_date = db.Column(db.String(length=4), nullable=False)
    artist_id = db.Column(db.Integer(), db.ForeignKey("artist.id"), nullable=False)
    genre_id = db.Column(db.Integer(), db.ForeignKey("genre.id"), nullable=False)
    artist = db.relationship("Artist", backref="album")
    genre = db.relationship("Genre", backref="album")
    link = db.relationship("Link", backref="album", cascade="all")

    def __repr__(self):
        return f"Album(id={self.id}, album_title={self.album_title}, release_date={self.released_date}," \
               f"artist_id={self.artist_id}, genre_id={self.genre_id})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=150), unique=True)
    password = db.Column(db.String(length=150))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.role = Role.query.filter_by(id=self.role_id).first()

    def action(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.action(Permission.ADMIN)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = Permission.COMMENT

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def __repr__(self):
        return f"Role({self.name}, {self.permissions})"

    @staticmethod
    def insert_roles():
        roles = {
            "User": [Permission.COMMENT],
            "Administrator": [Permission.ADMIN, Permission.COMMENT]
        }
        for role_key in roles.keys():
            role = Role.query.filter_by(name=role_key).first()
            if role is None:
                role = Role(name=role_key)
            role.reset_permissions()
            for perm in roles[role_key]:
                role.add_permission(perm)
            db.session.add(role)
        db.session.commit()
