from os import getcwd


port = 5000

url = f"http://localhost:{port}/"

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    # SECRET_KEY = environ.get('SECRET_KEY') DEAL WITH THIS LATER

    # Database setup for later
    
    directory = getcwd()
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{directory}/log.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False