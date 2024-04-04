from flask import Flask
from config.config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


csrf = CSRFProtect() #
app = Flask(__name__) # инициализируем приложение
app.config.from_object(Config) # передаем конфигурацию в приложение
csrf.init_app(app) # инициализируем защиту приложения
db = SQLAlchemy(app) # инициализируем бд с ORM
migrate = Migrate(app, db) # связываем приложение и бд
login = LoginManager(app) # инициализируем менеджер логинов
login.login_view = 'login' #  указываем имя функции для фхода в систему (куда перенаправляются незарегистрированные пользователи)

from app import routes, models # ! Обязательная строчка, без нее не подлкючаются виды, модели
# отправка дебага на электронную почту
import logging
from logging.handlers import SMTPHandler

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Sites error',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    # запись в лог файл
    import os
    from logging.handlers import RotatingFileHandler
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/INFO.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Site debug")