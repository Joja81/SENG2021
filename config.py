from os import getcwd, environ


port = 5000

url = f"http://localhost:{port}/"

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    # SECRET_KEY = environ.get('SECRET_KEY') DEAL WITH THIS LATER

    # Database setup for later
    environ['SMTP_HOST'] = 'smtp.gmail.com'
    environ['SMTP_PORT'] = '587'
    environ['SMTP_USERNAME'] = 'se2y22g21@gmail.com'
    environ['SMTP_PASSWORD'] = '&RLZJhYn!F7xBr'

    directory = getcwd()
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{directory}/log.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False