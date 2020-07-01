import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
# from hashids import Hashids
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app, name='User Administration', template_mode='bootstrap3')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
bootstrap = Bootstrap(app)
# hashids = Hashids(salt="Wl2MaNie68QIR0ai")

# def hashidEncode(x):
#     return hashids.encode(x)
#
# app.jinja_env.globals.update(hashidEncode=hashidEncode)

from app import views, models
