import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '-1')
   
    if SECRET_KEY == '-1':
        SECRET_KEY = secrets.token_hex(15)
        os.environ['SECRET_KEY'] = SECRET_KEY

    SQLALCHEMY_DATABASE_URI = "sqlite:///database/site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False