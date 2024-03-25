from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object('config')
csrf.init_app(app)
db = SQLAlchemy(app)

from app import views, models # ! Обязательная строчка, без нее не подлкючаются виды, модели