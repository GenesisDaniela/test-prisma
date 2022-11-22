from flask_restful import Resource
from flask import request, jsonify
from financialControl.schemas.bill_schema import billsSchema
from .....schemas.bill_schema import billSchema
from .....models.bill import Bill
from .....models.user import User
from datetime import datetime
from sqlalchemy.exc import NoResultFound, ArgumentError
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

class UserBillsIdResource(Resource):
    @cross_origin()
    @jwt_required()
    def get(self, username, bill_id):
        try:
            user = User.simple_filterByOne(username=username)
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
    @jwt_required()
    def delete(self, username, bill_id):
        try:
            user = User.simple_filterByOne(username=username) 
        except NoResultFound:
            return {'msg':f'user with username: \'{username}\' not found'}, 404
        try: 
            bill = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':'bill not found'}, 404
        if(user.id != bill.user_id):
            return {'msg':'user can only delete their own bills'}, 401
        Bill.delete(bill)
        return billsSchema.dump(Bill.get_all())
    
    @cross_origin()
    @jwt_required()
    def put(self, username, bill_id): #falta validar el username perteniciente a la bill
        try:
            user = User.simple_filterByOne(username=username) 
        except NoResultFound:
            return {'msg':f'user with username: \'{username}\' not found'}, 404
        try: 
            billFound = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':f'bill with id: \'{bill_id}\' of the user \'{username}\' not found'}, 404
        try:
            data = request.get_json()
            bill = Bill(billFound.id, billFound.date_bill, billFound.id_user, billFound.value, billFound.type, billFound.observation)
            if "type" in data:
                bill.type = data["type"]
            if "observation" in data:
                bill.observation = data["observation"]
            if "value" in data:
                bill.value = data["value"]
            if "date_bill" in data:
                bill.date_bill = datetime.strptime(data["date_bill"], '%Y-%m-%d').date()
        except:
            return {'mgs': 'Incorrect fields, try again'}, 400
        Bill.save(bill)
        return billSchema.dump(bill)
        