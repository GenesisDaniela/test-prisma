from flask_restful import Resource
from flask import request
from .....schemas.bill_schema import billsSchema, billSchema
from .....models.bill import Bill
from .....models.user import User
from sqlalchemy.exc import NoResultFound
from flask_cors import cross_origin
from financialControl.config.auth_middleware import token_required

class UserBillsResource(Resource):
    @cross_origin()
    @token_required
    def get(self,user): 
        try:
            user_found = User.simple_filterByOne(username=user)
            bills = Bill.simple_filter(user_id=user_found.id)
        except NoResultFound:
            return {f"user {user} not found"}, 404
        response = billsSchema.dump(bills)
        return response
    
    @cross_origin()
    @token_required
    def post(self,user):
        try:
            user_found = User.simple_filterByOne(username=user)
            data = request.get_json()
            bill = Bill(None, user_found.id, data["value"], data["type"], data["observation"])
        except Exception:
            return {'mgs': 'Incorrect fields, try again'}, 400
        Bill.save(bill)
        return billSchema.dump(bill)
    