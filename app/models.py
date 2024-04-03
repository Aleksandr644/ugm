from typing import TYPE_CHECKING
from app import db, login
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

ROLE_ADMIN = 0;
ROLE_USER = 1;

class Person(UserMixin, db.Model):
    """
    пользователи системы
    """
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(255)) # ФИО
    position = db.Column(db.String(255)) # должность
    birthday = db.Column(db.Date, default=datetime.date.today()) # день рождения
    login = db.Column(db.String(25), index=True, unique=True, nullable=False) # логин
    password = db.Column(db.String(255)) # пароль
    email = db.Column(db.String(255)) # электронная почта
    role = db.Column(db.SmallInteger, default=ROLE_USER) # Права
    about_me = db.Column(db.Text)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # realtionship
    #arrivals = db.relationship('Arrival', backref='responsible', lazy='dynamic')
    #expenses = db.relationship('Expense', backref='responsible', remote_side = [id_person])
    #recipients = db.relationship('Expense', backref='recipient', remote_side = [recipient])
    
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

class Product(db.Model):
    """
    продукты
    """
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key = True)
    article = db.Column(db.String(100), unique=True, index=True) # артикул продукта
    name = db.Column(db.String(255)) # название продукта
    description = db.Column(db.Text) # описание продукта
    volume = db.Column(db.Float) # вес продукта, количество шт в продукте, объем продукта и т.д.
    unit = db.Column(db.String(30)) # единицы измерения продукта шт, литров, кг и т.д.
    link = db.Column(db.String(255)) # ссылка на продукт
    id_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    # relationship
    #arrivals = db.relationship('Arrival', backref='product')
    #expenses = db.relationship('Expense', backref='product')
    
    __table_args__ = ()

    def __repr__(self):
        return f"<product {self.name}>"

class Category(db.Model):
    """
    категории продуктов
    """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), index=True) # Название категории
    description = db.Column(db.Text) # Описание категории
    #relationship
    #products = db.relationship('Product', backref='category')
    
    
    __table_args__ = ()

    def __repr__(self):
        return f"<category {self.name}>"

class Arrival(db.Model): 
    """
    поступление
    """
    __tablename__ = 'arrival'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow) # дата поступления
    id_product = db.Column(db.Integer, db.ForeignKey('product.id')) # поступивший продукт
    amount = db.Column(db.Integer, nullable=False) # колличество/позиций продукта
    id_person = db.Column(db.Integer, db.ForeignKey('person.id')) # ответственный за запись
    notes = db.Column(db.Text) # примечание
    
    __table_args__ = ()

    def __repr__(self):
        return f"<arrival {self.date}>"

class Expense(db.Model): 
    """
    выдача
    """
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow) # дата выдачи
    id_product = db.Column(db.Integer, db.ForeignKey('product.id')) # выданный продукт
    quantity = db.Column(db.Float) # колличество (шт, литров, кг)
    recipient = db.Column(db.Integer, db.ForeignKey('person.id')) # получатель
    id_person = db.Column(db.Integer, db.ForeignKey('person.id')) # ответственный
    notes = db.Column(db.Text) # примечание
    
    __table_args__ = ()

    def __repr__(self):
        return f"<expense {self.date}>"
# utcnow без вызова используеться для передачи функции и вызова на сервере при проведении записи

@login.user_loader # регистрация загрузчика для работы с Flask_login
def load_user(id): # ф-я для загрузки пользователя по идентификатору
    return Person.query.get(int(id)) # запрос у БД пользователя по ID