"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flaskext.markdown import Markdown
from flask_pagedown import PageDown
from flask_mail import Mail


app = Flask(__name__)

app.config['SECRET_KEY'] = 'a6114f50ec8b3727b938fa92a7f6b969'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SIMPLEMDE_JS_IIFE'] = True
app.config['SIMPLEMDE_USE_CDN'] = True
app.config['MAIL_SERVER']='mail.tichonet.co.il'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'noreply@tichonet.co.il'
app.config['MAIL_PASSWORD'] = '%Frk#x{IjMKg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

md = Markdown(app, safe_mode=True)

pagedown = PageDown(app)

mail = Mail(app)

import EzrahotSite.views
