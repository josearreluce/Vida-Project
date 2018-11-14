import unittest
import sys
sys.path.append('../../')
from app import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table

class TestCase(unittest.TestCase):

	def test_user_sign_up(self):
		username = "test_user_case_1"
		password = "test_user_case_1"
		with models.DatabaseConnection() as db:
			user_info = models.User(username=username, pswd=password)
			check_user = db.query(models.User).filter_by(username=username, pswd=password).count()
			# Check that user does not exist
			self.assertEqual(check_user, 0)

			db.add(user_info)
			db.commit()
			check_user_after = db.query(models.User).filter_by(username=username, pswd=password).count()
			# Check that user now exists
			self.assertEqual(check_user_after, 1)
			# User is deleted, since it is created for testing purposes
			db.query(models.User).filter_by(username=username).delete()
