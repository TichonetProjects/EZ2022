from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired
from EzrahotSite.models import User
from flask_mde import MdeField

class RegistrationForm(FlaskForm):
    first_name = StringField('שם פרטי',
                           validators=[DataRequired()]) # must be not empty
    last_name = StringField('שם משפחה',
                           validators=[DataRequired()]) # must be not empty
    email = StringField('אימייל',
                        validators=[DataRequired(), Email()]) # must be not empty and a valid email (user@domain)
    password = PasswordField('סיסמה', 
                        validators=[DataRequired()]) # must be not empty
    school_class = StringField('כיתה',
                                     validators=[DataRequired()]) # must be not empty
    submit = SubmitField('הירשם')

    """function to check if an email is already in use"""
    def validate_email(self, email):
        """query the email, and if it finds something raise an exception"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('כתובת המייל הזאת כבר בשימוש. אנא השתמש בכתובת מייל אחרת.')


class LoginForm(FlaskForm):
    email = StringField('אימייל',
                        validators=[DataRequired(), Email()]) # must be not empty and a valid email (user@domain)
    password = PasswordField('סיסמה', validators=[DataRequired()]) # must be not empty
    remember = BooleanField('זכור אותי')
    submit = SubmitField('התחבר')

class SubmitArticle(FlaskForm):
    heading = StringField('כותרת ראשית',
                            validators=[DataRequired()]) # must be not empty
    caption = StringField('כותרת משנה',
                            validators=[DataRequired()]) # must be not empty
    thumbnail = StringField('תמונת כיסוי')
    body = MdeField('תוכן הכתבה', 
                    validators=[InputRequired("Input required")]) # must be not empty
    submit = SubmitField('צור כתבה')