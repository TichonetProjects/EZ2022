from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired
from EzrahotSite.models import User
from flask_mde import MdeField

class RegistrationForm(FlaskForm):
    first_name = StringField('שם פרטי',
                           validators=[DataRequired()])
    last_name = StringField('שם משפחה',
                           validators=[DataRequired()])
    email = StringField('אימייל',
                        validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    school_class = StringField('כיתה',
                                     validators=[DataRequired()])
    submit = SubmitField('הירשם')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('כתובת המייל הזאת כבר בשימוש. אנא השתמש בכתובת מייל אחרת.')


class LoginForm(FlaskForm):
    email = StringField('אימייל',
                        validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    remember = BooleanField('זכור אותי')
    submit = SubmitField('התחבר')

class SubmitArticle(FlaskForm):
    heading = StringField('כותרת ראשית',
                            validators=[DataRequired()])
    caption = StringField('כותרת משנה',
                            validators=[DataRequired()])
    thumbnail = StringField('תמונת כיסוי',
                            validators=[DataRequired()])
    body = MdeField('תוכן הכתבה', 
                    validators=[InputRequired("Input required")])
    submit = SubmitField('שליחה')