from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
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

class EditProfileForm(FlaskForm):
    full_name = StringField("Фамилия Имя Отчество", validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=255)])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_full_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_full_name = original_full_name
        
    def validate_full_name(self, full_name):
        if full_name.data != self.original_full_name:
            user = Person.query.filter_by(full_name=self.full_name.data).first()
            if user is not None:
                raise ValidationError("Пользователь с таким ФИО уже сущестует")