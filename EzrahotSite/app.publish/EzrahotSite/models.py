from EzrahotSite import db, login_manager, app, md

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_login import current_user
from functools import wraps
from flask import request, redirect, url_for, flash
from flask_mail import Message


@login_manager.user_loader
def load_user(user_id):
    """interface with flask-login, returns User from user id"""
    return User.query.get(user_id)


class User(db.Model):
    __tablename__ = 'user' # users table name

    user_id = db.Column(db.Integer, primary_key=True) # user id; used in differentiating users and as a table primary key
    
    first_name = db.Column(db.String, nullable=False) # first name; user's first name and must be not null
    last_name = db.Column(db.String, nullable=False) # last name; user's last name and must be not null
    email = db.Column(db.String, nullable=False) # email; user's email and must be not null. used in sending emails and as another layer of differentiation between users
    password = db.Column(db.String, nullable=False) # password; user's password and must be not null. is encrypted
    
    school_class = db.Column(db.String, nullable=False) # school class; user's class and must be not null

    user_type = db.Column(db.String, nullable=False) # user type; user's type and must be not null. used in permission management, can be ADMIN, NOT APPROVED or USER

    def get_full_name(self):
        """returns user's full name"""
        return f"{self.first_name} {self.last_name}"

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
            
    def get_all_admins():
        """returns all users who are admins"""
        return (User.query.filter_by(user_type = "ADMIN"))

    def accept_user(self):
        """accepts the user and commits to db"""
        self.user_type = "USER"
        db.session.commit()

    def delete_user(self):
        """deletes user's row and commits to db"""
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    __tablename__ = 'article' # articles table name

    article_id = db.Column(db.Integer, primary_key=True) # article id; used in differentiating users and as a table primary key
    
    heading = db.Column(db.String, nullable=False) # heading; article's heading and must be not null. used as an heading
    caption = db.Column(db.String, nullable=False) # caption; article's caption and must be not null. used as a short caption on what's the article about

    thumbnail = db.Column(db.String, nullable=False) # thumbnail; article's thumbnail and must be not null. used as a URL to a thumbnail image

    body = db.Column(db.String, nullable=False) # body; article's body and must be not null. used as the article's content formatted in Markdown
    
    post_date = db.Column(db.String, nullable=False) # post date/ article's post date and must be not null. used as the creation date of the article
    accept_date = db.Column(db.String, nullable=True) # accept date; article's accept date and must be not null. used as the acception date of the article (when an admin accepted it)

    is_accepted = db.Column(db.Boolean, nullable=False) # is accepted; whether an article has been accepted or not and must be not null. used to check whether an article has been accepted or not

    author_id = db.Column(db.Integer, nullable=False) # author id; the user id of the article's author. used to check which user created the article
    acceptor_id = db.Column(db.Integer, nullable=True) # acceptor id; the user id of the admin who accepted the article. used to check which user accepted the article

    def is_active(self):
        """returns if article is accepted"""
        return self.is_accepted

    def get_url(self):
        """returns the article's url"""
        return f"tichonet.co.il/article/{self.article_id}"

    def get_author(self):
        """returns author user object"""
        return User.query.get(self.author_id)

    def get_acceptor(self):
        """returns acceptor user object"""
        return User.query.get(self.acceptor_id)

    def get_body(self, length, three_dots = False):
        "returns article body (without markdown)"
        return self.body[:length] + ("..." if three_dots else "")

    def get_all_articles():
        """returns all articles"""
        return db.session.query(Article).all()

    def get_all_accepted():
        """returns all accepted articles"""
        return Article.query.filter_by(is_accepted=True)

    def get_all_unaccepted():
        """returns all unaccepted articles"""
        return Article.query.filter_by(is_accepted=False)

    def get_all_user(author):
        """return all articles by a specific author"""
        return Article.query.filter_by(author_id=author)

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

"""creates an email message to notify a user that their article has been accepted"""
def acceptArticleMessage(article):
    """find the article author and create a new message object. fill the message object with a predefined template with the author's credentials"""
    article_author = article.get_author()
    message = Message(f"הכתבה שלך אושרה! {article.heading}", sender="noreply@tichonet.co.il", recipients=[article_author.email])
    
    message.body = 'הכתבה שלך "{}" אושרה על ידי מנהלי המערכת!\n\n כדי לראות את הכתבה לחצו כאן {}.'.format(article.heading, article.get_url())
    message.html = 'הכתבה שלך "{}" אושרה על ידי מנהלי המערכת!\n\n כדי לראות את הכתבה לחצו כאן {}.'.format(article.heading, article.get_url())

    return message

"""creates an email message to notify a user that they have been accepted to the user system"""
def acceptUserMessage(user):
    """create a new message object and fill it with a predefined template with the user's credentials"""
    message = Message(f"המשתמש שלך אושר!", sender="noreply@tichonet.co.il", recipients=[user.email])
    
    message.body = 'היי {}, המשתמש שלך באתר האזרחות של תיכונט אושר על ידי מנהלי המערכת! כדי להיכנס למערכת לחצו כאן {}.'.format(user.first_name, "tichonet.co.il/login")
    message.html = 'היי {}, המשתמש שלך באתר האזרחות של תיכונט אושר על ידי מנהלי המערכת! כדי להיכנס למערכת לחצו כאן {}.'.format(user.first_name, "tichonet.co.il/login")

    return message

"""creates an email message to notify an admin that a new user has registered"""
def newUserMessage(user):
    """create a new message object and fill it with a predefined template with the user's credentials"""
    message = Message(f"משתמש חדש מחכה לאישור!", sender="noreply@tichonet.co.il", recipients=[user.email for user in User.get_all_admins()])
    
    message.body = 'המשתמש "{}" מחכה לאישור המערכת. לחצו כאן כדי לאשר {}.'.format(user.get_full_name(), f"tichonet.co.il/acceptuser/{user.user_id}")
    message.html = 'המשתמש "{}" מחכה לאישור המערכת. לחצו כאן כדי לאשר {}.'.format(user.get_full_name(), f"tichonet.co.il/acceptuser/{user.user_id}")

    return message

"""creates an email message to notify an admin that new article has been created"""
def newArticleMessage(article):
    """find the article author and create a new message object. fill the message object with a predefined template with the author's credentials"""
    message = Message(f"כתבה חדשה מחכה לאישור!", sender="noreply@tichonet.co.il", recipients=[user.email for user in User.get_all_admins()])
    
    article_author = article.get_author()

    message.body = 'הכתבה "{}" על ידי {} מחכה לאישור המערכת. לחצו כאן כדי לאשר {}.'.format(article.heading, article_author.get_full_name(), f"tichonet.co.il/acceptarticle/{article.article_id}")
    message.html = 'הכתבה "{}" על ידי {} מחכה לאישור המערכת. לחצו כאן כדי לאשר {}.'.format(article.heading, article_author.get_full_name(), f"tichonet.co.il/acceptarticle/{article.article_id}")

    return message

"""function decorator for that restricts access to admin only endpoints"""
def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

"""remove unwanted features of a string (currently only strips whitespace)"""
def clean_string(string):
    return string.strip()