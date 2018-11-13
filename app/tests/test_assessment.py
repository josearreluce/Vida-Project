import unittest
import sys
sys.path.append('../assessment') # gets into proper file path

import assessment_simple_test as ast

class TestAssessment(unittest.TestCase):

    def setUp(self):
        self.list_cond = ast.condition_list
        self.graph = ast.state_network2
        self.correct_symptom = "Symptom_1"
        self.incorrect_symptom = "Symptom_3"
        self.correct_condition = "Condition_1"
        self.incorrect_conditon = "Condition_4"
        self.correct_successors = ast.start_assessment(self.correct_symptom)


