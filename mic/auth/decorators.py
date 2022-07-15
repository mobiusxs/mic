import functools

from flask import redirect, url_for
from mic.auth.user import is_authenticated, is_authorized, is_admin


def authentication_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if is_authenticated():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.logout'))
    return decorated_function


def authorization_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if is_authorized():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.logout'))
    return decorated_function


def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.logout'))
    return decorated_function
