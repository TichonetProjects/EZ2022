from EzrahotSite import db, login_manager

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class RegisterForm(FlaskForm):
    
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    school_class = StringField('school_class', validators=[DataRequired()])

class LoginForm(FlaskForm):
    pass

class User(db.Model):
    
    # PRIMARY KEY
    user_id = db.Column(db.Integer, primary_key=True)

    user_type = db.Column(db.String, nullable=False)


    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        return False

