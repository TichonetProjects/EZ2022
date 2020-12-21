from EzrahotSite import db, login_manager

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

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
        inactiveUsers = []
        for users in db.session.query(User).all():
            if not users.is_active():
                inactiveUsers.append(users)
        return inactiveUsers


class Article(db.Model):
    __tablename__ = 'article'

    article_id = db.Column(db.Integer, primary_key=True)
    
    heading = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    
    post_date = db.Column(db.String, nullable=False)
    accept_date = db.Column(db.String, nullable=True)

    is_accepted = db.Column(db.Boolean, nullable=False)

    # author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # acceptor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def get_articles():
        articlesList = []
        for articles in db.session.query(Article).all()[:5]:
            articlesList.append(articles)
        return articlesList


