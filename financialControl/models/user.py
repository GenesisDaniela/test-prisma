from ..config.db import db,BaseModelMixin 
from ..config.ma import ma

class User(db.Model, BaseModelMixin):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True, nullable=False)
    username=db.Column(db.String(50))
    password=db.Column('pass',db.String(500))
    email=db.Column(db.String(100))

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __repr__(self):
        return f'User id:{self.id} username:{self.username} email:{self.email} clave:{self.password}'
