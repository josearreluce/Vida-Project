import unittest
import sys
import networkx
import datetime
sys.path.append('../assessment')   # gets into proper file path
sys.path.append('../src')
import assessment_simple_test as ast
from users import  *
import math
sys.path.append('../../')
from app import models

class TestUser(unittest.TestCase):

	# User Information
	def setUp(self):
		self.account = AccountInfo("username", "password")
		self.basicinfo = BasicInfo(10, "M")
		self.personalinfo = PersonalInfo(50, 120)
		self.hbg = HealthBackground(0.0, (80, 120), 1)
		self.user = User(self.account, self.basicinfo, self.personalinfo, self.hbg)

	def test_get_accountinfo(self):
		self.assertEqual(self.user.getAccountInfo(), self.account)

	def test_set_username(self):
		test_acc = AccountInfo("test_username", "test_password")
		self.user.setAccountInfo(test_acc)
		self.assertEqual(self.user.getAccountInfo(), test_acc)

	def test_get_basicinfo(self):
		self.assertEqual(self.user.getBasicInfo(), self.basicinfo)

	def test_set_basicinfo(self):
		test_bi = BasicInfo(11, "F")
		self.user.setBasicInfo(test_bi)
		self.assertEqual(self.user.getBasicInfo(), test_bi)

	def test_get_personalinfo(self):
		self.assertEqual(self.user.getPersonalInfo(), self.personalinfo)

	def test_set_personalinfo(self):
		test_pi = PersonalInfo(60, 130)
		self.user.setPersonalInfo(test_pi)
		self.assertEqual(self.user.getPersonalInfo(), test_pi)

	def test_get_healthbackground(self):
		self.assertEqual(self.user.getHealthBackground(), self.hbg)

	def test_set_healthbackground(self):
		test_hbg = HealthBackground(1.0, (90, 130), 2)
		self.user.setHealthBackground(test_hbg)
		self.assertEqual(self.user.getHealthBackground(), test_hbg)

class TestAccountInfo(unittest.TestCase):

	# Account Information
	def setUp(self):
		self.account = AccountInfo("username", "password")

	def test_get_username(self):
		self.assertEqual(self.account.getUsername(), "username")

	def test_set_username(self):
		self.account.setUsername("test_username")
		self.assertEqual(self.account.getUsername(), "test_username")

	def test_get_password(self):
		self.assertEqual(self.account.getPassword(), "password")

	def test_set_password(self):
		self.account.setPassword("test_password")
		self.assertEqual(self.account.getPassword(), "test_password")

class TestBasicInfo(unittest.TestCase):

	# Basic Information
	def setUp(self):
		self.basicinfo = BasicInfo(10, "M")

	def test_get_age(self):
		self.assertEqual(self.basicinfo.getAge(), 10)

	def test_set_age(self):
		self.basicinfo.setAge(20)
		self.assertEqual(self.basicinfo.getAge(), 20)

	def test_get_sex(self):
		self.assertEqual(self.basicinfo.getSex(), "M")

	def test_set_sex(self):
		self.basicinfo.setSex("F")
		self.assertEqual(self.basicinfo.getSex(), "F")

class TestPersonalInfo(unittest.TestCase):

	# Personal Information
	def setUp(self):
		self.personalinfo = PersonalInfo(50, 120)

	def test_get_height(self):
		self.assertEqual(self.personalinfo.getHeight(), 50)

	def test_set_height(self):
		self.personalinfo.setHeight(20)
		self.assertEqual(self.personalinfo.getHeight(), 20)

	def test_get_weight(self):
		self.assertEqual(self.personalinfo.getWeight(), 120)

	def test_set_weight(self):
		self.personalinfo.setWeight(130)
		self.assertEqual(self.personalinfo.getWeight(), 130)

class TestHealthBackground(unittest.TestCase):

	# Personal Information
	def setUp(self):
		self.hbg = HealthBackground(0.0, (80, 120), 1)

	def test_get_smoker(self):
		self.assertEqual(self.hbg.getSmoker(), 0.0)

	def test_set_smoker(self):
		self.hbg.setSmoker(1.0)
		self.assertEqual(self.hbg.getSmoker(), 1.0)

	def test_get_bloodpressure(self):
		self.assertEqual(self.hbg.getBloodPressure(), (80, 120))

	def test_set_bloodpressure(self):
		self.hbg.setBloodPressure((90, 130))
		self.assertEqual(self.hbg.getBloodPressure(), (90, 130))

	def test_get_diabetes(self):
		self.assertEqual(self.hbg.getDiabetes(), 1)

	def test_set_diabetes(self):
		self.hbg.setDiabetes(2)
		self.assertEqual(self.hbg.getDiabetes(), 2)

# Function to convert sqlalchemy database User class to backend User class
class TestDbUsertoUser(unittest.TestCase):

	def setUp(self):
		self.username = 'test_username'
		self.password = 'test_password'
		with models.DatabaseConnection() as db:
			count = db.query(models.UserSchema).filter_by(username=self.username).count()
			if count >= 1:
				user_info = models.UserSchema(username=self.username, pswd=self.password)
				db.query(models.UserSchema).filter_by(username=self.username).delete()
				db.commit()
		self.database_user = models.UserSchema(username=self.username, pswd=self.password)

	def test_dbuser_to_user(self):
		backend_user = DbUsertoUser(self.database_user)
		account = AccountInfo("username", "password")
		basicinfo = BasicInfo(10, "M")
		personalinfo = PersonalInfo(50, 120)
		hbg = HealthBackground(0.0, (80, 120), 1)
		user = User(self.account, self.basicinfo, self.personalinfo, self.hbg)
		self.assertEqual(backend_user, user)
