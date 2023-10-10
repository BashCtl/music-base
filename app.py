from src import create_app, db
from src.models.models import Role

app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        Role.insert_roles()
    app.run(host="0.0.0.0", debug=True)
