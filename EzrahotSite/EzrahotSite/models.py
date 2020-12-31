from EzrahotSite import db, login_manager, app

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_login import current_user
from functools import wraps
from flask import request, redirect, url_for, flash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    school_class = db.Column(db.String, nullable=False)

    user_type = db.Column(db.String, nullable=False)

    # article = db.relationship("Article")



    def is_active(self):
        """True, as all users are active."""
        return not self.user_type == "Wating_For_Aprrove"

    def get_all_inactive():
        return (User.query.filter_by(user_type = "Waiting_For_Aprrove"))
            

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        return False
    
    def is_admin(self):
        return self.user_type == "Admin_User"

    def get_inactive_users():
        return (User.query.filter_by(user_type="Wating_For_Aprrove"))

    def acceptUser(self):
        self.user_type = "Normal_User"
        db.session.commit()

    def deleteUser(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    __tablename__ = 'article'

    article_id = db.Column(db.Integer, primary_key=True)
    
    heading = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    
    post_date = db.Column(db.String, nullable=False)
    accept_date = db.Column(db.String, nullable=True)

    is_accepted = db.Column(db.Boolean, nullable=False)

    author_id = db.Column(db.Integer, nullable=False)
    acceptor_id = db.Column(db.Integer, nullable=True)

    def get_articles():
        articlesList = []
        for articles in db.session.query(Article).all()[:5]:
            articlesList.append(articles)
        return articlesList

    def is_active(self):
        return self.is_accepted
    
    def get_all_active():
        return (Article.query.filter_by(is_accepted=True))

    def get_inactive_articles():
        return (Article.query.filter_by(is_accepted=False))

    def acceptArticle(self):
        self.is_accepted = True
        self.accept_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.acceptor_id = current_user.user_id
        db.session.commit()

    def deleteArticle(self):
        db.session.delete(self)
        db.session.commit()


def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        print(current_user.first_name)
        if not current_user.is_admin():
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view