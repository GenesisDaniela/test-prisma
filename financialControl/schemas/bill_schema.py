from ..config.ma import ma
from ..models.bill import Bill
from ..schemas.user_schema import UserSchema

class BillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bill
    user = ma.Function(lambda obj: obj.user.username)
        
billSchema = BillSchema()
billsSchema = BillSchema(many=True)