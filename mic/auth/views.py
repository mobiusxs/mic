import base64
import json
import secrets
import time
import urllib.parse

from flask import abort, Blueprint, make_response, redirect, render_template, request, url_for
import requests

from mic.auth.user import is_authenticated, is_authorized, is_admin
from mic import config

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')


@auth.app_context_processor
def auth_context():
    """Add in-template context values."""

    return {
        'is_authenticated': is_authenticated(),
        # 'is_authorized': is_authorized(),
        'is_admin': is_admin(),
    }


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/')
def authorize():
    """Redirect the user to the Eve Online SSO server.
    Include values required by auth flow.
    """

    if is_authenticated():
        return redirect(url_for(config.LOGIN_REDIRECT_VIEW))
    state = secrets.token_urlsafe(32)
    data = {
        'response_type': 'code',
        'redirect_uri': config.EVE_CALLBACK_URL,
        'client_id': config.EVE_CLIENT_ID,
        'scope': config.EVE_SCOPE,
        'state': state
    }
    location = f'https://login.eveonline.com/v2/oauth/authorize/?{urllib.parse.urlencode(data)}'
    response = make_response(redirect(location=location, code=302))
    response.set_cookie('state', state)
    return response


@auth.route('/callback')
def callback():
    """Handle the callback portion of the SSO auth flow.
    User will have authenticated and authorized the app via Eve Online's SSO server.
    A JWT will be returned.
    That JWT is parsed and required values are stored as cookies.
    """

    # validate state
    request_state = request.args.get('state')
    cookie_state = request.cookies.get('state')
    if request_state != cookie_state:
        abort(400)

    # get JWT
    code = request.args.get('code')
    url = 'https://login.eveonline.com/v2/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }
    basic = base64.urlsafe_b64encode(f'{config.EVE_CLIENT_ID}:{config.EVE_SECRET_KEY}'.encode('utf-8')).decode()
    headers = {
        'Authorization': f'Basic {basic}'
    }
    sso_response = requests.post(url=url, data=data, headers=headers)
    sso_response.raise_for_status()
    jwt = sso_response.json()

    # create response
    response = make_response(redirect(url_for(config.LOGIN_REDIRECT_VIEW)))
    response.set_cookie('state', '', expires=0)

    # parse jwt
    header, raw_payload, signature = jwt['access_token'].split('.')

    # parse payload
    payload = base64.b64decode(raw_payload + '==')
    payload = json.loads(payload)
    name = payload['name']
    character_id = payload['sub'].split(':')[2]

    # get character
    esi_response = requests.get(f'https://esi.evetech.net/latest/characters/{character_id}/?datasource=tranquility')
    esi_response.raise_for_status()
    character = esi_response.json()
    corporation_id = character['corporation_id']
    alliance_id = character['alliance_id']

    # set cookies
    response.set_cookie('expiry', str(int(time.time()) + int(jwt['expires_in'] - 10)))
    response.set_cookie('refresh_token', jwt['refresh_token'])
    response.set_cookie('header', header)
    response.set_cookie('payload', raw_payload)
    response.set_cookie('signature', signature)
    response.set_cookie('name', name)
    response.set_cookie('character_id', character_id)
    response.set_cookie('corporation_id', str(corporation_id))
    response.set_cookie('alliance_id', str(alliance_id))
    return response


@auth.route('/logout')
def logout():
    """Delete all cookies and redirect to configured view"""

    response = make_response(redirect(url_for(config.LOGOUT_REDIRECT_VIEW)))
    cookies = [
        'expiry',
        'refresh_token',
        'header',
        'payload',
        'signature',
        'name',
        'character_id',
        'corporation_id',
        'alliance_id'
    ]
    for cookie in cookies:
        response.set_cookie(cookie, '', expires=0)
    return response