from flask import Flask
from flask_wtf.csrf import CSRFProtect
from postgreDB import PGDB

csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object('config')
csrf.init_app(app)

from app import views, models # ! Обязательная строчка, без нее не подлкючаются виды