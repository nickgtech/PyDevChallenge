from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = 'user'
    username = db.Column('username', db.String(16), primary_key=True)
    password = db.Column('password', db.String(60))
    authenticated = db.Column('authenticated', db.Boolean, default=False)

    # Overrides UserMixin get_id
    def get_id(self):
        return (self.username)


class UserGif(db.Model):

    __tablename__ = 'user_gifs'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(16))
    gif_url = db.Column('gif_url', db.String(200))
    category = db.Column('category', db.String(45))


class Keys(db.Model):

    __tablename__ = 'keys'
    name = db.Column('name', db.String(100), primary_key=True)
    key = db.Column('key', db.String(100))
