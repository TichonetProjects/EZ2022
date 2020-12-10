from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
from EzrahotSite.models import User

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
            raise ValidationError('That email is taken. Please choose a different one.')