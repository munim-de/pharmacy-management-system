from flask import abort
from flask_login import current_user
from functools import wraps

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.role not in roles:
                return abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
