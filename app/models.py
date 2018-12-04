from app import app
from app import db
from app import login
from sqlalchemy.dialects.postgresql import JSON
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class DatabaseConnection():

    def __init__(self):
        self.db = None
        self.uri = app.config['SQLALCHEMY_DATABASE_URI']

    def open(self):
        engine = sqlalchemy.create_engine(self.uri)
        session = sessionmaker()
        session.configure(bind=engine)
        self.db = session()

    def __enter__(self):
        self.open()
        return self.db

    def close(self):
        if not self.db:
            raise Exception('DatabaseConnection was not created properly')
        self.db.close()

    def __exit__(self, exception_type, value, traceback):
        if not self.db:
            raise Exception('DatabaseConnection was not created properly')
        self.close()


class UserSession(UserMixin, db.Model):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    pswd = Column(String)
    age = Column(Integer)
    sex = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    smoker = Column(Float)
    diabetes = Column(Integer)
    blood_pressure_low = Column(Integer)
    blood_pressure_high = Column(Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        salt = app.config['SALT']
        self.pswd = generate_password_hash(password + salt)

    def check_password(self, password):
        salt = app.config['SALT']
        return check_password_hash(self.pswd, password + salt)

    def get_id(self):
        return self.username

class AssessmentHistory():
    __tablename__ = 'users'

    username = Column(String)
    pswd = Column(String)

@login.user_loader
def load_user(username):
    return UserSession.query.get(username)

