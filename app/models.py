from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Customers(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    login: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    phone: so.Mapped[str] = so.mapped_column(sa.String(12))
    employee: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    administrator: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    bids: so.WriteOnlyMapped['Bids'] = so.relationship(back_populates='customer')
    comments: so.WriteOnlyMapped['Comments'] = so.relationship(back_populates='customer')
    products: so.WriteOnlyMapped['Logs_product'] = so.relationship(back_populates='customer')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        if self.password:
            return check_password_hash(self.password, password)
        else: return False
    
    def __repr__(self):
        return f''

class Bids(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    customer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Customers.id))
    date: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    date_close: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True) 
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    customer: so.Mapped['Customers'] = so.relationship(back_populates='bids')
    
    def __repr__(self):
        return f''

class Comments(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    bid_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Bids.id))
    customer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Customers.id))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    date: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    customer: so.Mapped['Customers'] = so.relationship(back_populates='comments')
    
    def __repr__(self):
        return f''

class Products(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    count: so.Mapped[int] = so.mapped_column(sa.Integer)
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda:datetime.now(timezone.utc))
    logs: so.WriteOnlyMapped['Logs_product'] = so.relationship( back_populates='product')

    def __repr__(self):
        return f''

class Logs_product(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    customer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Customers.id))
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Products.id))
    count: so.Mapped[int] = so.mapped_column(sa.Integer)
    date: so.Mapped[datetime] = so.mapped_column(default=lambda:datetime.now(timezone.utc))
    product: so.Mapped['Products'] = so.relationship(back_populates='logs')
    customer: so.Mapped['Customers'] = so.relationship(back_populates='products')
    
    def __repr__(self):
        return f''

@login.user_loader
def load_user(id):
    return db.session.get(Customers, int(id))