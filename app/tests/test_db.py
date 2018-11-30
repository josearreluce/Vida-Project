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
		self.no_table = "select * from doctors"
		self.no_column = "select doctors from conditions"
		self.wrong_syntax = "* select from conditions"
		self.no_value = "select * from conditions where sex=100"
		self.right_value = "select name from conditions where cond_id='cond_1'"

		# for test cases iteration 2
		self.cond_right_val = "select sub_sympt_4 from conditions where cond_id='cond_4'"
		self.sub_right_val = "select sub_sympt_21 from related_symptoms where sympt_id='sympt_1'"
		self.sub_wrong_val_no_probability = "select name from related_symptoms where sympt_id='sympt_1' and sub_sympt_1=0"
		self.sub_wrong_val_certain_probability = "select name from related_symptoms where sympt_id='sympt_1' and (sub_sympt_5=1 or sub_sympt_1=1)"
		self.sub_wrong_val_not_subsymptom = "select name from related_symptoms where sympt_id='sympt_2' and (sub_sympt_5!=0 or sub_sympt_1!=0)" 
		self.sub_no_val = "select sub_sympt_120 from related_symptoms where sympt_id='sympt_1'"
		self.valid_age = "select name from conditions where cond_id = 'cond_3' and age_min=0 and age_max=100"
		self.invalid_age = "select name from conditions where cond_id = 'cond_5' and age_min=18 and age_max=40"
		self.valid_time = "select name from conditions where cond_id = 'cond_3' and time_min=7 and time_max=10"
		self.invalid_time = "select name from conditions where cond_id = 'cond_5' and time_min=3 and time_max=5"

	def test_right_query(self):
		self.assertRaises(AssertionError, self.assertRaises, pg2.ProgrammingError, self.cur.execute, self.good_query)

	def test_no_table(self):
		self.assertRaises(pg2.ProgrammingError, self.cur.execute, self.no_table)

	def test_no_column(self):
		self.assertRaises(pg2.ProgrammingError, self.cur.execute, self.no_column)

	def test_wrong_syntax(self):
		self.assertRaises(pg2.ProgrammingError, self.cur.execute, self.wrong_syntax)

	def test_no_return_value(self):
		self.assertIsNone(self.cur.execute(self.no_value))

	def test_right_value(self):
		self.cur.execute(self.right_value)
		value = self.cur.fetchall()[0][0]
		self.assertEqual(value, 'apendicitis')

	#test cases iteration 2. This tests the general restructuring of the database that we imposed for this iteration

	#there is no sub_sympt_120, therefore this should return None
	def test_sub_no_val(self):
		self.assertRaises(pg2.ProgrammingError, self.cur.execute, self.sub_no_val)

	#if sub_sympt_1 is a sub symptom of sympt_1, then ther is no condition where sympt_id='sympt_1' and sub_sympt_1=0
	def test_sub_wrong_val_no_probability(self):
		self.assertIsNone(self.cur.execute(self.sub_wrong_val_no_probability))

	#if sub_sympt_5 and sub_symptom_1 are subsymptoms of sympt_1 then neither of them can have probability = 1
	def test_sub_wrong_val_certain_probability(self):
		self.assertIsNone(self.cur.execute(self.sub_wrong_val_certain_probability))

	#if sub_sympt_5 and sub_symptom_1 are subsymptoms of sympt_1 then they cannot be subsymptoms of sympt_2, so they must = 0
	def test_sub_wrong_val_not_subsymptom(self):
		self.assertIsNone(self.cur.execute(self.sub_wrong_val_not_subsymptom))

	def test_invalid_age(self):
		self.assertIsNone(self.cur.execute(self.invalid_age))

	def test_invalid_time(self):
		self.assertIsNone(self.cur.execute(self.invalid_time))

	def test_cond_right_val(self):
		self.cur.execute(self.cond_right_val)
		value = self.cur.fetchall()[0][0]
		self.assertEqual(value, 0.5)

	def test_sub_right_val(self):
		self.cur.execute(self.sub_right_val)
		value = self.cur.fetchall()[0][0]
		self.assertEqual(value, 0.125)

	def test_valid_age(self):
		self.cur.execute(self.valid_age)
		value = self.cur.fetchall()[0][0]
		self.assertEqual(value, "common cold")

	def test_valid_time(self):
		self.cur.execute(self.valid_time)
		value = self.cur.fetchall()[0][0]
		self.assertEqual(value, "common cold")