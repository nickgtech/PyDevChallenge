from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectField, BooleanField, HiddenField
from wtforms.validators import InputRequired, Length, EqualTo

class GifForm(FlaskForm):

    category = SelectField('category', choices=[('Food', 'Food'),
                                                ('Funny', 'Funny'),
                                                ('Animals', 'Animals'),
                                                ('Sports','Sports'),
                                                ('Movies', 'Movies'),
                                                ('Fail', 'Fail'),
                                                ('Weird', 'Weird'),
                                                ('Dance', 'Dance')])
    urlHidden = HiddenField('url')

class RegistrationForm(FlaskForm):

    username = StringField('username', validators=[InputRequired('A username is required!'),
                                                   Length(min=8, max=16,
                                                          message="Must be between 8 and 16 characters")])
    password = PasswordField('password', validators=[InputRequired('A password is required!'),
                                                   Length(min=8, max=16,
                                                          message="Must be between 8 and 16 characters"),
                                                     EqualTo('pass_match', message='Passwords must match')])
    pass_match = PasswordField('Confirm Password')
    recaptcha = RecaptchaField()


class SearchForm(FlaskForm):

    search = StringField('', validators=[InputRequired()])

class LoginForm(FlaskForm):

    username = StringField('username', validators=[InputRequired(), Length(max=16)])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember me')
    recaptcha = RecaptchaField()


class FilterForm(FlaskForm):

    category = SelectField('Show', choices=[('all', 'All'),
                                                ('food', 'Food'),
                                                ('funny', 'Funny'),
                                                ('animals', 'Animals'),
                                                ('sports', 'Sports'),
                                                ('movies', 'Movies'),
                                                ('fail', 'Fail'),
                                                ('weird', 'Weird'),
                                                ('dance', 'Dance')])

