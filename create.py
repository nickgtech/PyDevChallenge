from flask import Flask
from flask_login import LoginManager
from Models import Keys, db

# Get the Secret keys needed from the keys table
def get_key(name, app):

    # SQLAlchemy works with the current Application Context of a view.
    # It needs to be provided if its used outside of a view
    with app.app_context():
        # Query for and return a key object by name
        key_obj = Keys.query.filter_by(name=name).first()
        return key_obj.key


# Create the app object with keys and configs
def create_app():

    app = Flask(__name__)

    # Created sqlite db for easier install and run for demo.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggiphy.db'

    # init the sqlalchemy extension
    db.init_app(app)

    # uncomment for connection with local mysql db
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:33060/ggiphy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = get_key('SECRET_KEY', app)
    app.config['RECAPTCHA_PUBLIC_KEY'] = get_key('RECAPTCHA_PUBLIC_KEY', app)
    app.config['RECAPTCHA_PRIVATE_KEY'] = get_key('RECAPTCHA_PRIVATE_KEY', app)
    return app


# handles flask-login init
def create_login_manager(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    # links flask-login mechanisms to a view
    login_manager.login_view = 'login'

    return login_manager