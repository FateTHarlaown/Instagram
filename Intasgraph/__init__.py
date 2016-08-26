# -*- coding: utf-8 -*-
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
app.secret_key = 'zhang is sily B'
login_manager = LoginManager(app)
login_manager.login_view = '/relogin/'
login_manager.login_message = u'请先登录'
db = SQLAlchemy(app)

from Intasgraph import models, views

