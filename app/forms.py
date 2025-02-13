from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField,TelField, DateField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional, Regexp
import sqlalchemy as sa
from app import db
from app.models import Customers
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить вход?')
    submit = SubmitField('Войти', render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired("Поле должно быть заполнено")])
    email = StringField('Электронная почта', validators=[DataRequired("Поле должно быть заполнено"), Email("В поле должна быть электронная почта")])
    password = PasswordField('Пароль', validators=[DataRequired("Поле должно быть заполнено")])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired("Поле должно быть заполнено"), EqualTo('password', message='Пароли должны совпадать')])
    first_name = StringField("Имя", validators=[DataRequired("Поле должно быть заполнено")])
    last_name = StringField("Фамилия", validators=[DataRequired("Поле должно быть заполнено")])
    phone = TelField("Телефон", validators=[DataRequired("Поле должно быть заполнено"),Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="должен быть номер телефона")])
    employee = BooleanField("Работник", validators=[Optional()])
    administrator = BooleanField("Администратор", validators=[Optional()])
    description = TextAreaField("Дополнительная информация", validators=[Optional()])
    submit = SubmitField('Готово', render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(Customers).where(Customers.login == username.data))
        if user is not None:
            raise ValidationError(' Пожалуйста, используйте другой логин.')
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(Customers).where(Customers.email == email.data))
        if user is not None:
            raise ValidationError('Пожалуйста, введите другую электронную почту.')

class CreateBidForm(FlaskForm):
    description = TextAreaField("Текст заявки", validators=[DataRequired('Поле должно быть заполнено')], render_kw={'style': 'height: 280px; width:500px;'})
    submit = SubmitField('Отправить', render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})

class BidCommentForm(FlaskForm):
    text = StringField("Комментировать")
    submit = SubmitField('Отправить', render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})
    

class BidsForm(FlaskForm):
    open = BooleanField("Только открытые")
    id = StringField("По номеру заявки")
    submit = SubmitField("Поиск", render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})
    
class ChangeForm(FlaskForm):
    email = StringField('Электронная почта', validators=[Optional(),Email("В поле должна быть электронная почта")])
    password2 = PasswordField('Новый пароль')
    confirm = PasswordField('Повторите пароль', validators=[EqualTo('password2', message='Пароли должны совпадать')])
    first_name = StringField("Имя")
    last_name = StringField("Фамилия")
    phone = TelField("Телефон", validators=[Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="должен быть номер телефона")])
    description = TextAreaField("Дополнительная информация", validators=[Optional()])
    password = PasswordField('Старый Пароль', validators=[DataRequired("Поле должно быть заполнено")])
    submit = SubmitField('Сохранить', render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(Customers).where(Customers.email == email.data))
        if user is not None and not current_user == user:
            raise ValidationError('Пожалуйста, введите другую электронную почту.')

class ProductsForm(FlaskForm):
    name = StringField('Название')
    submit = SubmitField("Найти", render_kw={'id':"header-top-right-signin", 'style':"margin: auto;"})