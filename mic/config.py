from os import environ
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent

EVE_CLIENT_ID = environ.get('EVE_CLIENT_ID')
EVE_SECRET_KEY = environ.get('EVE_SECRET_KEY')
EVE_CALLBACK_URL = environ.get('EVE_CALLBACK_URL')
EVE_SCOPE = environ.get('EVE_SCOPE')

SECRET_KEY = environ.get('SECRET_KEY')

LOGIN_REDIRECT_VIEW = 'dashboard.index'
LOGOUT_REDIRECT_VIEW = 'auth.login'

SQLALCHEMY_DATABASE_URI = f'sqlite:///{ROOT}/db.sqlite3'
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
