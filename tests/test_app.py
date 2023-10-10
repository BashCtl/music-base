import pytest
from flask import url_for, g
from src.models.models import Genre


def test_home_page(client):
    response = client.get("/home")
    assert b"Music Box" in response.data


def test_admin_login_page(client):
    response = client.get("/main/dude/login")
    assert b"Dudes Login" in response.data


def test_admin_valid_login(client, admin):
    response = client.post("/main/dude/login", data={
        "username": admin["username"],
        "password": admin["password"]
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Administration" in response.data
    assert b"Adding new artist" in response.data


@pytest.mark.parametrize("username, password, expected", [
    ("fakename", "password123", b"<strong> User doesn&#39;t exist.</strong>"),
    ("bigjoe", "fakepassword", b"<strong> Dude, it&#39;s not correct password! Try again!</strong>")
])
def test_invalid_admin_login(client, admin, username, password, expected):
    response = client.post("/main/dude/login", data={
        "username": username,
        "password": password
    })
    assert expected in response.data


# def test_add_new_genre(auth_client, app):
#
#     with app.app_context():
#         response = auth_client.post("/main/dude/new_genre", data={"add_genre": "Rock"})
#
#         print(response)
#         assert Genre.query.count() == 1
