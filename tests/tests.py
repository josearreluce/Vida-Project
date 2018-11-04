import unittest
import sys
sys.path.append('../src') # gets into proper file path

from testthis import multiply,add
from condition import Condition
from symptom import Symptom
from users import User #users.py is pluralized because just user is another existing module.


# This is just test case, remove later
class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_numbers_3_4(self):
        self.assertEqual( multiply(3,4), 12)

    def test_strings_a_3(self):
        self.assertEqual( multiply('a',3), 'aaa')

    def test_add_3_4(self):
        self.assertEqual(add(3,4), 7)

    def test_add_a_b(self):
        self.assertEqual(add("a","b"), "ab")



class TestConditionClass(unittest.TestCase):

    def setUp(self):
        self.condition = Condition("Description", [], "name", "id", "sex")

    def test_get_symptoms(self):
        self.assertEqual(self.condition.getSymptoms(), [])



class TestUserClass(unittest.TestCase):

    def setUp(self):
        self.user = User("username", "password", 1, 18)

    def test_startAssessment(self):
        self.assertEqual(self.user.startAssessment(), 0)

    def test_logout(self):
        self.assertEqual(self.user.logout(), 0)



class TestSymptomClass(unittest.TestCase):
    def setUp(self):
        self.symptom = Symptom("name", 0, 0, [], [], "description")

    def test_get_related_symptoms(self):
        self.assertEqual(self.symptom.getRelatedSymptoms(), [])

    def test_get_conditions(self):
        self.assertEqual(self.symptom.getConditions(), [])

    def test_get_desc(self):
        self.assertEqual(self.symptom.getDesc(), "description")







if __name__ == '__main__':
    unittest.main()
