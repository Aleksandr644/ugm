from flask import Flask
from config.config import Config

from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)
csrf.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models # ! Обязательная строчка, без нее не подлкючаются виды, модели