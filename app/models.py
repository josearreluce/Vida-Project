from app import app
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

class DatabaseConnection():

    def __init__(self):
        self.db = None
        self.uri = app.config['SQLALCHEMY_DATABASE_URI']

    def __enter__(self):
        engine = sqlalchemy.create_engine(self.uri)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.db = Session()
        return self.db

    def __exit__(self, exception_type, value, traceback):
        if not self.db:
            raise Exception('DatabaseConnection was not created properly')
        self.db.close()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    pswd = Column(String)

