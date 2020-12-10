from EzrahotSite import db, login_manager

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model):
    
    # PRIMARY KEY
    user_id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    school_class = db.Column(db.String, nullable=False)

    user_type = db.Column(db.String, nullable=False)



    def is_active(self):
        """True, as all users are active."""
        if User.query.get(user_type) != "Wating_For_Approve":
            return True
        else:
            return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        return False

