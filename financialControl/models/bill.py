from ..config.db import db,BaseModelMixin 
from ..config.ma import ma
from datetime import datetime
class Bill(db.Model, BaseModelMixin):
    __tablename__ = 'bill'
    id=db.Column(db.Integer, primary_key=True, nullable=False)
    date_bill=db.Column(db.Date)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_ = db.Column('type',db.Integer,  nullable=False)
    value=db.Column(db.Integer,  nullable=False)
    observation = db.Column(db.String(120),  nullable=False)
    user = db.relationship("User")
    
    def __init__(self, id, user_id, value, type_, observation):
        self.id = id
        self.date_bill = datetime.now()
        self.user_id = user_id
        self.value = value
        self.type_ = type_
        self.observation = observation
    
    def __repr__(self):
        return f'Bill id:{self.id} date:{self.date_bill} user_id:{self.user_id} type:{self.type_} value:{self.value} observation:{self.observation}'