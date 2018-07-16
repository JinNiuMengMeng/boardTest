from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError


class checkboxForm(FlaskForm):
    number1 = StringField('UserName', validators=[DataRequired()])
    number2 = PasswordField("Password", validators=[DataRequired()])
    number3 = BooleanField("RememberMe")
    submit = SubmitField('Log In')
