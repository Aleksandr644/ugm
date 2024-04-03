from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Person

class  LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_userusername(self, username): # проверка по шаблону validate_<имя проверяемого поля>
        user = Person.query.filter_by(login = username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким логином уже есть.')
    
    def validate_email(self, email):
        user = Person.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Такая электронная почта уже есть.')