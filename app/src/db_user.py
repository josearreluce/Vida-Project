from sqlalchemy import Column, Integer, String

class User(Base):
	__tablename__ = 'users'

		username = Column(String, primary_key=True)
		password = Column(String)

		def __repr__(self):
			return "<User(username='%s', password='%s')>" % 
			(self.username, self.password)