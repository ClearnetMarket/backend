

from flask_login import current_user
from flask import abort

from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            pass
        else:
            abort(401)
        return f(*args, **kwargs)

    return decorated_function
