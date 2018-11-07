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
        self.condition = Condition("Description", [], "name", -1, 0)

    def test_get_symptoms(self):
        self.assertEqual(self.condition.getSymptoms(), [])



class TestUserClass(unittest.TestCase):

    def setUp(self):
        self.user = User("username", "password", 1, 18)

    def test_startAssessment(self):
        self.assertEqual(self.user.startAssessment(), 0)

    def test_logout(self):
        self.assertEqual(self.user.logout(), 0)

    def test_set_name(self):
        self.user.setName("Patient1")
        self.assertEqual("Patient1", self.user.getName())

    def test_set_id(self):
        self.user.setId(9999)
        self.assertEqual(9999, self.user.getId())

    def test_set_date_of_birth(self):
        self.user.setDateOfBirth("06-13-1956")
        self.assertEqual("06-13-1956", self.user.getDateOfBirth())

    def test_set_height(self):
        self.user.setHeight(180)
        self.assertEqual(180, self.user.getHeight())

    def test_set_weight(self):
        self.user.setWeight(200)
        self.assertEqual(200, self.user.getWeight())

    def test_add_preexisting_condition(self):
        cond = Condition("Runny nose and sneezing", [], "flu", 19283, 0)
        self.assertEqual([], self.user.getPreExistingConditions())
        self.user.addPreExistingCondition(cond)
        self.assertEqual(cond, self.user.getPreExistingConditions()[0])



class TestSymptomClass(unittest.TestCase):
    def setUp(self):
        self.condition = Condition("Condition1", [], "name", -1, 0)
        self.symptom = Symptom("name", 0, 0, [self.condition], [], "description")

    def test_get_related_symptoms(self):
        self.assertEqual(self.symptom.getRelatedSymptoms(), [])

    def test_get_conditions(self):
        self.assertEqual(self.symptom.getConditions(), [self.condition])

    def test_get_desc(self):
        self.assertEqual(self.symptom.getDesc(), "description")







if __name__ == '__main__':
    unittest.main()
