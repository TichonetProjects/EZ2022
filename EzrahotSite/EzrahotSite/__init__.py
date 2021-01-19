"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_misaka import Misaka
from flask_mde import Mde

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a6114f50ec8b3727b938fa92a7f6b969'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SIMPLEMDE_JS_IIFE'] = True
app.config['SIMPLEMDE_USE_CDN'] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

md = Misaka()
md.init_app(app)

mde = Mde(app)

import EzrahotSite.views
