
from flask import jsonify, session
import functools
from app.classes.auth import Auth_User


def login_required(functionin):
    @functools.wraps(functionin)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return functionin(*args, **kwargs)
    return secure_function

def vendor_account_required(functionin):
    @functools.wraps(functionin)
    def secure_function(*args, **kwargs):
        user_id = session.get("user_id")
        get_user = Auth_User.query.filter(Auth_User.id == user_id).first()
        if get_user.vendor_account == 0:
            return jsonify({"error": "Unauthorized"}), 401
        return functionin(*args, **kwargs)
    return secure_function

