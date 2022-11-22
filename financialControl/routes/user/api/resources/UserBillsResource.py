from flask_restful import Resource
from flask import request
from financialControl.config.auth_middleware import token_required
from .....schemas.bill_schema import billsSchema, billSchema
from .....models.bill import Bill
from .....models.user import User
from sqlalchemy.exc import NoResultFound
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
class UserBillsResource(Resource):
    @cross_origin()
    @token_required
    def get(self,user): 
        """returns a user's list bill of the logged in user 
    ---
    tags:
      - User
    parameters:
      - name: user
        in: path
        type: string
        required: true
    definitions:
      BillResponse:
        type: object
        properties:
          id:
            type: integer
          date_bill:
            type: string
            format: date
          value:
            type: integer
          type:
            type: integer
          observation:
            type: string     
    responses:
      201:
        description: A list bills
        schema:
          $ref: '#/definitions/BillResponse'
    """
        try:
            user_found = User.simple_filterByOne(username=user)
            bills = Bill.simple_filter(user_id=user_found.id)
            print("XXXXXXXx")
        except NoResultFound:
            return {f"user {user} not found"}, 404
        response = billsSchema.dump(bills)
        return response
    
    @cross_origin()
    @token_required
    def post(self,user):
        """returns a user's bill of the logged in user identified by bill id
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Bill'
      - name: user
        in: path
        type: string
        required: true
    definitions:
      BillResponse:
        type: object
        properties:
          id:
            type: integer
          date_bill:
            type: string
            format: date
          value:
            type: integer
          type:
            type: integer
          observation:
            type: string            
      Bill:
        type: object
        properties:
          value:
            type: integer
          type:
            type: integer
          observation:
            type: string 
    responses:
      201:
        description: A bill
        schema:
          $ref: '#/definitions/BillResponse'
    """
        try:
            user_found = User.simple_filterByOne(username=user)
            data = request.get_json()
            bill = Bill(None, user_found.id, data["value"], data["type"], data["observation"])
        except Exception:
            return {'mgs': 'Incorrect fields, try again'}, 400
        Bill.save(bill)
        return billSchema.dump(bill)
    