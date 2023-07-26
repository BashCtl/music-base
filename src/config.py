from dotenv import load_dotenv
from os import getenv


class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = getenv("SECRET_KEY")
