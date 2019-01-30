from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class LoginForm(FlaskForm):

    username = StringField('username', validators=[InputRequired('A username is required!'),
                                                   Length(min=8, max=16,
                                                          message="Must be between 8 and 16 characters")])
    email = StringField('email', validators=[InputRequired('An email is required!'), Email()])
    password = PasswordField('password', validators=[InputRequired('A password is required!'),
                                                   Length(min=8, max=16,
                                                          message="Must be between 8 and 16 characters")])
    pass_match = PasswordField('pass_match', validators=[InputRequired('Password is Required!'),
                                                   Length(min=8, max=16,
                                                          message="Must be between 8 and 16 characters")])
    recaptcha = RecaptchaField()
