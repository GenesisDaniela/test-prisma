from ..config.ma import ma
from ..models.bill import Bill
from ..schemas.user_schema import UserSchema
from marshmallow import fields

class BillSchema(ma.Schema):
    user = fields.Nested(UserSchema(only=("username",), many=False))
    id=fields.Integer()
    date_bill=fields.Date()
    user_id=fields.Integer()
    type_ = fields.Integer()
    value=fields.Integer()
    observation = fields.String()   
billSchema = BillSchema()
billsSchema = BillSchema(many=True)