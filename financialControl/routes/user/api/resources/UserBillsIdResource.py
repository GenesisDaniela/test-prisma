from flask_restful import Resource
from flask import request, jsonify
from financialControl.schemas.bill_schema import billsSchema
from financialControl.config.auth_middleware import token_required
from .....schemas.bill_schema import billSchema
from .....models.bill import Bill
from .....models.user import User
from datetime import datetime
from sqlalchemy.exc import NoResultFound, ArgumentError
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

class UserBillsIdResource(Resource):
    @cross_origin()
    @token_required
    def get(self, user, bill_id):
        """returns the bills of the logged in user identified by bill id
    ---
    tags:
      - User
    parameters:
      - name: bill_id
        in: path
        type: integer
        required: true
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
        description: User logged
        schema:
          $ref: '#/definitions/BillResponse'
    """
        try:
            user = User.simple_filterByOne(username=user)
        except NoResultFound:
            return {'msg':f'user with username: \'{user}\' not found'}, 404
        try:
            bill = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':'bill not found'}, 404
        if(user.id != bill.user_id):
            return {'msg':'user can only get their own bills'}, 401
        return billSchema.dump(bill)
    
    @cross_origin()
    @token_required
    def delete(self, user, bill_id):
        """delete and returns a user's bill of the logged in user identified by bill id
    ---
    tags:
      - User
    parameters:
      - name: bill_id
        in: path
        type: integer
        required: true
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
        description: A list bills
        schema:
          $ref: '#/definitions/BillResponse'
    """
        try:
            user = User.simple_filterByOne(username=user) 
        except NoResultFound:
            return {'msg':f'user with username: \'{user}\' not found'}, 404
        try: 
            bill = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':'bill not found'}, 404
        if(user.id != bill.user_id):
            return {'msg':'user can only delete their own bills'}, 401
        Bill.delete(bill)
        return billsSchema.dump(Bill.get_all())
    
    @cross_origin()
    @token_required
    def put(self, user, bill_id): 
        """update and returns a user's bill of the logged in user identified by bill id
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Bill'
      - name: bill_id
        in: path
        type: integer
        required: true
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
        description: Bill updated
        schema:
          $ref: '#/definitions/BillResponse'
    """
        try:
            user = User.simple_filterByOne(username=user) 
        except NoResultFound:
            return {'msg':f'user with username: \'{user}\' not found'}, 404
        try: 
            billFound = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':f'bill with id: \'{bill_id}\' of the user \'{user}\' not found'}, 404
        try:
            data = request.get_json()
            if "type" in data:
                billFound.type_ = data["type"]
            if "observation" in data:
                billFound.observation = data["observation"]
            if "value" in data:
                billFound.value = data["value"]
        except:
            return {'mgs': 'Incorrect fields, try again'}, 400
        Bill.update(billFound)
        return billSchema.dump(billFound)