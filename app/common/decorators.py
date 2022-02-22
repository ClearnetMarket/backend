

from flask_login import current_user
from flask import redirect, url_for, request
from app import db
from functools import wraps
from app.classes.auth import Auth_User

from datetime import datetime


def admin_account_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin == 0:
            return redirect(url_for('index', next=request.url))
        else:
            pass
        return f(*args, **kwargs)
    return decorated_function


def admin_account_level_required_3(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin_role >= 3:
            pass
        else:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def ADMINaccountlevel4_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin_role >= 4:
            pass
        else:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_account_required_level_10(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin_role >= 10:
            pass
        else:
            return redirect(url_for('index', next=request.url))

        return f(*args, **kwargs)
    return decorated_function




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.username == 'Guest':
            return redirect(url_for('auth.login', next=request.url))
        else:
            pass
        if current_user.is_authenticated:
            pass
        else:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def vendoraccount_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.vendor_account == 1:
            pass
        else:
            return redirect(url_for('index', next=request.url))

        return f(*args, **kwargs)
    return decorated_function
