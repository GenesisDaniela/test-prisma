from flask import Blueprint
from flask_restful import Api
from financialControl.routes.auth.api.resources.authResource import AuthResource

auth_api = Blueprint('auth_api', __name__)
api = Api(auth_api)

api.add_resource(AuthResource, '/login', endpoint='login_resource')
