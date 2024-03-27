from typing import TYPE_CHECKING
from app import db
from datetime import date

ROLE_ADMIN = 0;
ROLE_USER = 1;

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    birthday = db.Column(db.Date, default=date.today())
    login = db.Column(db.String(25), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    
    def __repr__(self):
        return f"<User {self.login}>"
    
    