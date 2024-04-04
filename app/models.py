from typing import Optional, List
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship

from app import db, login
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

ROLE_ADMIN = 0;
ROLE_USER = 1;

class Person(UserMixin, DeclarativeBase):
    """
    пользователи системы
    """
    __tablename__ = 'person'
    
    id = mapped_column(sa.Integer, primary_key = True)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    full_name = mapped_column(sa.String(255)) # ФИО
    position = mapped_column(sa.String(255)) # должность
    birthday = mapped_column(sa.Date, default=datetime.date.today()) # день рождения
    login = mapped_column(sa.String(25), index=True, unique=True, nullable=False) # логин
    password = mapped_column(sa.String(255)) # пароль
    email = mapped_column(sa.String(255)) # электронная почта
    role = mapped_column(sa.SmallInteger, default=ROLE_USER) # Права
    about_me = mapped_column(sa.Text)
    last_seen = mapped_column(sa.DateTime, default=datetime.datetime.utcnow)
    # realtionship
    arrivals = relationship('Arrival', backref='responsible', lazy='dynamic')
    expenses = relationship('Expense',primaryjoin= backref='responsible')
    recipients = relationship('Expense', backref='recipient')
    
    __table_args__ = ()
    
    def __repr__(self):
        return f"<User {self.login}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Product(sa.Model):
    """
    продукты
    """
    __tablename__ = "product"
    id = mapped_column(sa.Integer, primary_key = True)
    article = mapped_column(sa.String(100), unique=True, index=True) # артикул продукта
    name = mapped_column(sa.String(255)) # название продукта
    description = mapped_column(sa.Text) # описание продукта
    volume = mapped_column(sa.Float) # вес продукта, количество шт в продукте, объем продукта и т.д.
    unit = mapped_column(sa.String(30)) # единицы измерения продукта шт, литров, кг и т.д.
    link = mapped_column(sa.String(255)) # ссылка на продукт
    id_category = mapped_column(sa.Integer, sa.ForeignKey('category.id'))
    # relationship
    arrivals = relationship('Arrival', backref='product')
    expenses = relationship('Expense', backref='product')
    
    __table_args__ = ()

    def __repr__(self):
        return f"<product {self.name}>"

class Category(sa.Model):
    """
    категории продуктов
    """
    __tablename__ = 'category'
    id = mapped_column(sa.Integer, primary_key = True)
    name = mapped_column(sa.String(255), index=True) # Название категории
    description = mapped_column(sa.Text) # Описание категории
    #relationship
    products = sa.relationship('Product', backref='category')
    
    
    __table_args__ = ()

    def __repr__(self):
        return f"<category {self.name}>"

class Arrival(sa.Model): 
    """
    поступление
    """
    __tablename__ = 'arrival'
    id = mapped_column(sa.Integer, primary_key = True)
    date = mapped_column(sa.DateTime, index=True, default=datetime.datetime.utcnow) # дата поступления
    id_product = mapped_column(sa.Integer, sa.ForeignKey('product.id')) # поступивший продукт
    amount = mapped_column(sa.Integer, nullable=False) # колличество/позиций продукта
    id_person = mapped_column(sa.Integer, sa.ForeignKey('person.id')) # ответственный за запись
    notes = mapped_column(sa.Text) # примечание
    
    __table_args__ = ()

    def __repr__(self):
        return f"<arrival {self.date}>"

class Expense(sa.Model): 
    """
    выдача
    """
    __tablename__ = 'expense'
    id = mapped_column(sa.Integer, primary_key = True)
    date = mapped_column(sa.DateTime, index=True, default=datetime.datetime.utcnow) # дата выдачи
    id_product = mapped_column(sa.Integer, sa.ForeignKey('product.id')) # выданный продукт
    quantity = mapped_column(sa.Float) # колличество (шт, литров, кг)
    recipient = mapped_column(sa.Integer, sa.ForeignKey('person.id')) # получатель
    id_person = mapped_column(sa.Integer, sa.ForeignKey('person.id')) # ответственный
    notes = mapped_column(sa.Text) # примечание
    
    __table_args__ = ()

    def __repr__(self):
        return f"<expense {self.date}>"
# utcnow без вызова используеться для передачи функции и вызова на сервере при проведении записи

@login.user_loader # регистрация загрузчика для работы с Flask_login
def load_user(id): # ф-я для загрузки пользователя по идентификатору
    return Person.query.get(int(id)) # запрос у БД пользователя по ID