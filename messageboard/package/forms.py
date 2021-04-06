"""
Managing forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from package.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2, max=16)]
    )
    password = PasswordField('Password',
        validators=[DataRequired(),Length(min=5, max=25)]
    )
    confirmpassword = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username taken! :(")

class LoginForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2, max=16)]
    )
    password = PasswordField('Password',
        validators=[DataRequired(),Length(min=5, max=25)]
    )
    remember = BooleanField('Remember?')
    submit = SubmitField("Login")
        
class ProfileForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2, max=16)]
    )
    password = PasswordField('Password',
        validators=[DataRequired(),Length(min=5, max=25)]
    )
    submit = SubmitField("Change")
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username taken! :(")