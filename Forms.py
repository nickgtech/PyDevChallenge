from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectField, BooleanField, HiddenField
from wtforms.validators import InputRequired, Length, EqualTo


class GifForm(FlaskForm):

    # Form that handles saving a Gif for the user.
    # Creates a select box and hidden field.
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

    # User Registration Form.
    # Uses validators to ensure data provided is valid.
    # Creates a username field and two password fields that must match.
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

    # Simple search form with a search field
    search = StringField('', validators=[InputRequired()])


class LoginForm(FlaskForm):

    # Login form
    # Creates a username and password textfield
    # As well as a Recaptcha for better CSRF protection and remember me field for flask-login
    username = StringField('username', validators=[InputRequired(), Length(max=16)])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember me')
    recaptcha = RecaptchaField()


class FilterForm(FlaskForm):

    # Simple select box for gif filtering in the profile
    category = SelectField('Show', choices=[('all', 'All'),
                                                ('Food', 'Food'),
                                                ('Funny', 'Funny'),
                                                ('Animals', 'Animals'),
                                                ('Sports', 'Sports'),
                                                ('Movies', 'Movies'),
                                                ('Fail', 'Fail'),
                                                ('Weird', 'Weird'),
                                                ('Dance', 'Dance')])

