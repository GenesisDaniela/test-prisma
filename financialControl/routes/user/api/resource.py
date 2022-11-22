from flask import Blueprint
from flask_restful import Api
from ....schemas.bill_schema import BillSchema
from financialControl.routes.user.api.resources.UserBillsResource import UserBillsResource
from financialControl.routes.user.api.resources.UserBillsIdResource import UserBillsIdResource

user_api = Blueprint('user_api', __name__)
bill_schema = BillSchema()
api = Api(user_api)

api.add_resource(UserBillsIdResource, '/<string:username>/bills/<int:bill_id>', endpoint='user_bill_resource')
api.add_resource(UserBillsResource, '/<string:user>/bills', endpoint='user_list_resource')
