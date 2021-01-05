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
        """returns if user type is anything else than NOT_APPROVED"""
        return not self.user_type == "NOT_APPROVED"


    def is_authenticated(self):
        """returns true if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """returns false as all users are not anonymous"""
        return False
    
    def is_admin(self):
        """returns if the user is admin"""
        return self.user_type == "ADMIN"

    def get_id(self):
        """returns user id"""
        return self.user_id

    def get_all_inactive():
        """returns all users who are not approved"""
        return (User.query.filter_by(user_type = "NOT_APPROVED"))
            

    def accept_user(self):
        """accepts the user and commits to db"""
        self.user_type = "USER"
        db.session.commit()

    def delete_user(self):
        """deletes user's row and commits to db"""
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    __tablename__ = 'article'

    article_id = db.Column(db.Integer, primary_key=True)
    
    heading = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=False)

    thumbnail = db.Column(db.String, nullable=False)

    body = db.Column(db.String, nullable=False)
    
    post_date = db.Column(db.String, nullable=False)
    accept_date = db.Column(db.String, nullable=True)

    is_accepted = db.Column(db.Boolean, nullable=False)

    author_id = db.Column(db.Integer, nullable=False)
    acceptor_id = db.Column(db.Integer, nullable=True)

    def is_active(self):
        """returns if article is accepted"""
        return self.is_accepted

    def get_all_articles():
        """returns all articles"""
        return db.session.query(Article).all()

    def get_all_accepted():
        """returns all accepted articles"""
        return Article.query.filter_by(is_accepted=True)

    def get_all_unaccepted():
        """returns all unaccepted articles"""
        return Article.query.filter_by(is_accepted=False)

    
    def accept_article(self):
        """accepts article and commits to db"""
        self.is_accepted = True
        self.accept_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.acceptor_id = current_user.user_id
        db.session.commit()

    def delete_article(self):
        """deletes article and commits to db"""
        db.session.delete(self)
        db.session.commit()


"""function decorator for admin only pages"""
"""TODO currently calls unauthorized if not admin instead of custom stuff but we are lazy :3"""
def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view