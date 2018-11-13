from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	username = Column(String, primary_key=True)
	password = Column(String)

	# def __repr__(self):
	# 	return "<User(username='%s', password='%s')>" % 
	# 	(self.username, self.password)