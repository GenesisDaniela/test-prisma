from flask_restful import Resource
from flask import request
from .....models.user import User
from sqlalchemy.exc import NoResultFound
import jwt

class AuthResource(Resource):
    
    def post(self):
        """Login user
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/LoginInfo'
    definitions:
      LoginInfo:
        type: object
        properties:
          username:
            type: string
          pass:
            type: string
      LoginResponse:
        type: object
        properties:
          login:
            type: boolean
          username:
            type: string
          email:
            type: string
          mensaje:
            type: string
          token:
            type: string
    responses:
      201:
        description: User logged
        schema:
          $ref: '#/definitions/LoginResponse'
    """
        try:
            print(User.get_all())
            data = request.get_json()
            if not data:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            try:
                is_validated = User.simple_filterByOne(username=data['username'], password= data['pass'])
                print(is_validated)
            except Exception:
                return {
                    "login":False,
                    "mensaje":"Usuario o contraseña inválido"
                }, 404
                
            if is_validated is None:
                return dict(message='Invalid data', data=None, error=is_validated), 400
            user ={
                "id": is_validated.id,
                "username":data["username"],
                "password":data["pass"]
                }
            if user:
                token = jwt.encode(
                    {"user_id": user["id"]},
                    key="token",
                    algorithm="HS256"
                )
                return {
                    "login": True,
                    "username": is_validated.username,
                    "email": is_validated.email,
                    "mensaje": "Welcome",
                    "token": "Bearer "+token
                }
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
                    "data": None
            }, 500
            