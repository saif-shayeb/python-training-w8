from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims.get("role") not in required_roles:
                roles_str = ", ".join(required_roles)
                abort(
                    403,
                    description=f"Forbidden: Requires one of the following roles: {roles_str}",
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator
