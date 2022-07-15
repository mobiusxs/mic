from flask import request


def is_authenticated():
    required_cookies = [
        'name',
        'character_id',
        'corporation_id',
        'alliance_id',
        'expiry',
        'refresh_token',
    ]
    for cookie in required_cookies:
        if not request.cookies.get(cookie):
            return False
    return True


def is_authorized():
    if not is_authenticated():
        return False
    # TODO: Implement check for authorization
    # example: check if character, corporation, alliance ID in whitelist
    raise NotImplementedError


def is_admin():
    if not is_authenticated():
        return False
    # TODO: Implement admin check
    # example: check if character in admin list
    raise NotImplementedError


def get_user():
    user = {
        'name': request.cookies.get('name'),
        'character_id': request.cookies.get('character_id'),
        'corporation_id': request.cookies.get('corporation_id'),
        'alliance_id': request.cookies.get('alliance_id'),
    }
    return user
