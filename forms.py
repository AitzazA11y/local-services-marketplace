from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RequestForm(FlaskForm):
    client_name = StringField('Your Name', validators=[DataRequired(), Length(max=50)])
    contact = StringField('Phone or Email', validators=[DataRequired(), Length(max=50)])
    message = TextAreaField('What do you need done?', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Request')

class RegisterForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')