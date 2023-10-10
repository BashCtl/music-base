import pytest
from dotenv import load_dotenv
from os import getenv, getcwd
from src import create_app, db
from src.forms.forms import SearchForm
from src.models.models import User, Role
from werkzeug.security import generate_password_hash


class TestConfig:
    load_dotenv()
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("TEST_DATABASE_URI")
    WTF_CSRF_ENABLED = False


@pytest.fixture()
def app():
    app = create_app(TestConfig)

    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

    with app.app_context():
        db.create_all()
        Role.insert_roles()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin(app):
    data = {"username": "bigjoe", "password": "password123", "role_id": "2"}
    with app.app_context():
        user = User(username=data["username"], password=generate_password_hash(data["password"]),
                    role_id=data["role_id"])
        db.session.add(user)
        db.session.commit()
    return data


@pytest.fixture()
def auth_client(client, admin):
    response = client.post("/main/dude/login", data={
        "username": admin["username"],
        "password": admin["password"]
    }, follow_redirects=True)
    assert b"Administration" in response.data
    return client
