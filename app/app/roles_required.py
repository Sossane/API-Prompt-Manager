from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role_id'] not in roles:
                return jsonify({'error': 'Access denied. You do not have permission to access this resource.'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
