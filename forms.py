from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class RequestForm(FlaskForm):
    client_name = StringField('Your Name', validators=[DataRequired(), Length(max=50)])
    contact = StringField('Phone or Email', validators=[DataRequired(), Length(max=50)])
    message = TextAreaField('What do you need done?', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Request')