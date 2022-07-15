from os import environ

from dotenv import load_dotenv

load_dotenv()

EVE_CLIENT_ID = environ.get('EVE_CLIENT_ID')
EVE_SECRET_KEY = environ.get('EVE_SECRET_KEY')
EVE_CALLBACK_URL = environ.get('EVE_CALLBACK_URL')
EVE_SCOPE = environ.get('EVE_SCOPE')

LOGIN_REDIRECT_VIEW = 'dashboard.index'
LOGOUT_REDIRECT_VIEW = 'auth.login'
