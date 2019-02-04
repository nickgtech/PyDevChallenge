from flask import Flask
from flask_login import LoginManager
from Models import Keys, db


def get_key(name, app):

    with app.app_context():
        key_obj = Keys.query.filter_by(name=name).first()
        return key_obj.key


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggiphy.db'
    db.init_app(app)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:33060/ggiphy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = get_key('SECRET_KEY', app)
    app.config['RECAPTCHA_PUBLIC_KEY'] = get_key('RECAPTCHA_PUBLIC_KEY', app)
    app.config['RECAPTCHA_PRIVATE_KEY'] = get_key('RECAPTCHA_PRIVATE_KEY', app)
    return app


def create_login_manager(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return login_manager