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