from flask_restful import Resource
from flask import request
from financialControl.dto.login_info_dto import LoginInfoDTO
from .....models.user import User
from sqlalchemy.exc import NoResultFound
import jwt

class AuthResource(Resource):
    def post(self):
        try:
            print(User.simple_filter)
            data = request.get_json()
            if not data:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            try:
                is_validated = User.simple_filterByOne(username=data['username'], password= data['pass'])
                # print(is_validated)
                # print(User.simple_filter)
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
                    "token": token
                }
        except Exception as e:
            return {
                    "message": "Something went wrong!",
                    "error": str(e),
                    "data": None
            }, 500
            