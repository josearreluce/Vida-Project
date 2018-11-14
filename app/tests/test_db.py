import psycopg2 as pg2
import unittest

# Tests to make sure database is set up correctly
class TestConn(unittest.TestCase):

	def setUp(self):
		self.right_host = 'ec2-13-59-75-157.us-east-2.compute.amazonaws.com'
		self.wrong_host = 'localhost'
		self.right_user = 'pv_admin'
		self.wrong_user = 'admin'
		self.right_db = 'pv_db'
		self.wrong_db = 'db_pv'
		self.right_passwd = 'CMSC22001'
		self.wrong_passwd = 'CMSC2200'

	def test_right_creds(self):
		arg1 = 'host=%s dbname=%s user=%s password=%s'%(self.right_host, self.right_db, self.right_user, self.right_passwd)
		self.assertRaises(AssertionError, self.assertRaises, pg2.OperationalError, pg2.connect, arg1)

	def test_wrong_host(self):
		arg1 = 'host=%s dbname=%s user=%s password=%s'%(self.wrong_host, self.right_db, self.right_user, self.right_passwd)
		self.assertRaises(pg2.OperationalError, pg2.connect, arg1)

	def test_wrong_db(self):
		arg1 = 'host=%s dbname=%s user=%s password=%s'%(self.right_host, self.wrong_db, self.right_user, self.right_passwd)
		self.assertRaises(pg2.OperationalError, pg2.connect, arg1)

	def test_wrong_user(self):
		arg1 = 'host=%s dbname=%s user=%s password=%s'%(self.right_host, self.right_db, self.wrong_user, self.right_passwd)
		self.assertRaises(pg2.OperationalError, pg2.connect, arg1)

	def test_wrong_passwd(self):
		arg1 = 'host=%s dbname=%s user=%s password=%s'%(self.right_host, self.right_db, self.right_user, self.wrong_passwd)
		self.assertRaises(pg2.OperationalError, pg2.connect, arg1)

# Test if we can retrieve information from database
class TestQuery(unittest.TestCase):

	def setUp(self):
		self.conn = pg2.connect('host=ec2-13-59-75-157.us-east-2.compute.amazonaws.com dbname=pv_db user=pv_admin password=CMSC22001')
		self.cur = self.conn.cursor()
		self.good_query = "select * from conditions"
		self.no_column = "select * from doctors"
		self.wrong_syntax = "* select from conditions"
		self.no_value = "select * from conditions where sex=100"

	def test_right_query(self):
		self.assertRaises(AssertionError, self.assertRaises, pg2.ProgrammingError, self.cur.execute, self.good_query)

	def test_no_column(self):
		self.assertRaises(pg2.ProgrammingError, self.cur.execute, self.no_column)

	def test_wrong_syntax(self):
		self.assertRaises(pg2.ProgrammingError, self.cur.execute, self.wrong_syntax)

	def test_no_return_value(self):
		self.assertIsNone(self.cur.execute(self.no_value))
		