import sqlalchemy as db
from sqlalchemy import Column

from base import Base


class User(Base):

    __tablename__ = 'user'
    password = Column('password', db.String(16))
    username = Column('username', db.String(16))
    email = Column('email', db.String(50),primary_key=True)
    authenticated = Column('authenticated', db.Boolean, default=False)

    def __init__(self, password, username,
                 email, authenticated):
        self.password = password
        self.username = username
        self.email = email
        self.authenticated = authenticated

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_first_name(self, last_name):
        self.first_name = last_name

    def is_authenticated(self):
        return self.authenticated

    def set_authenticated(self, auth):
        self.authenticated = auth