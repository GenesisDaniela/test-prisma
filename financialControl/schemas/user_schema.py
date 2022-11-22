from ..config.ma import ma
from ..models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
userSchema = UserSchema()
usersSchema = UserSchema(many=True)