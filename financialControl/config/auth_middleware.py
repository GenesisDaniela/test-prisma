from base64 import b64decode
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from ..models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing! , please log in via /login and paste the token",
                "error": "Unauthorized"
            }, 401
        try:
            jwt_options = {
            'verify_signature': False,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
            }
            
            data=jwt.decode(
                token,
                algorithms=["HS256"],
                options=jwt_options
                )
            current_user = User.get_by_id(data["user_id"])
        except Exception as e:
            return {
                "message": "Invalid Authentication token!",
                "error": "Unauthorized"
            }, 401
        return f(*args , **kwargs)
    return decorated