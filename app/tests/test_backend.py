import unittest
import sys
sys.path.append('../src') # gets into proper file path

from condition import Condition
from symptom import Symptom
from users import User #users.py is pluralized because just user is another existing module.

# Test conditions
class TestConditionClass(unittest.TestCase):

    def setUp(self):
        self.condition = Condition("Description", [], "name", -1, 0)

    #Retrieve list of symptoms
    def test_get_symptoms(self):
        self.assertEqual(self.condition.getSymptoms(), [])

    # Generate next question in diagnosis
    def test_get_question(self):
        self.assertEqual(self.condition.getNextQuestion(), "question")

# Test User profile information
class TestUserClass(unittest.TestCase):

    def test_startAssessment(self):
        self.assertEqual(self.user.startAssessment(), 0)

    # User information will be iumplemented in iteration 2
    def test_set_name(self):
        self.user.setName("Patient1")
        self.assertEqual("Patient1", self.user.getName())

    def test_set_date_of_birth(self):
        self.user.setDateOfBirth("06-13-1956")
        self.assertEqual("06-13-1956", self.user.getDateOfBirth())

    def test_set_height(self):
        self.user.setHeight(180)
        self.assertEqual(180, self.user.getHeight())

    def test_set_weight(self):
        self.user.setWeight(200)
        self.assertEqual(200, self.user.getWeight())

    def test_set_gender(self):
        self.user.setGender(180)
        self.assertEqual(180, self.user.getGender())

    def test_add_preexisting_condition(self):
        cond = Condition("Runny nose and sneezing", [], "flu", 19283, 0)
        self.assertEqual([], self.user.getPreExistingConditions())
        self.user.addPreExistingCondition(cond)
        self.assertEqual(cond, self.user.getPreExistingConditions()[0])

    # See assessment history
    def test_get_history(self):
        self.assertEqual([], self.user.getHistory())

# Tests symptoms
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

    def test_get_desc(self):
        self.assertEqual(self.symptom.getDesc(), "description")

if __name__ == '__main__':
    unittest.main()
