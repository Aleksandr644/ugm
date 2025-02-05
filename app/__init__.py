from flask import Flask
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

# модуль фласк
app = Flask(__name__)
app.config.from_object(Config)

# модуль базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# модуль проверки авторизации пользователя.
login = LoginManager(app)
login.login_view = 'login'

moment = Moment(app)

from app import routes, models