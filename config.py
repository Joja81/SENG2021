from os import getcwd, environ
import os
import enviro

port = 5000

url = f"http://localhost:{port}/"

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    if 'SECRET_KEY' in environ:
        SECRET_KEY = environ.get('SECRET_KEY')

    # Database setup for later

    directory = getcwd()
    
    if "DATABASE_URL" in os.environ: # Gets uri for databse from eviro if on heroku, otherwise uses local sqlite
        db_start = os.environ.get("DATABASE_URL")
        split_db = db_start.split(":")
        split_db[0] += "ql"
        SQLALCHEMY_DATABASE_URI = ":".join(split_db)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:////{directory}/log.db"

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False