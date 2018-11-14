import unittest
import sys
import networkx
sys.path.append('../assessment')   # gets into proper file path
import assessment_simple_test as ast


class TestAssessment(unittest.TestCase):

    def setUp(self):
        self.list_cond = ast.condition_list
        self.graph = ast.state_network2
        self.correct_symptom = "Symptom_1"
        self.incorrect_symptom = "Symptom_3"
        self.correct_condition = "Condition_1"
        self.incorrect_condition = "Condition_4"
        self.correct_successors = ast.start_assessment(self.correct_symptom)
        self.user_sub_answers = [0, 1]

        self.correct_symptom2 = "Symptom_2"
        self.correct_condition2 = "Condition_2"
        self.correct_successors2 = ast.start_assessment(self.correct_symptom2)

        self.correct_symptom3 = "Sub1_symptom_1"


    #All fails, or none applicable: returns an empty list
    #Success: returns ALL candidate conditions
    def test_input_check(self):
        self.assertTrue(ast.verify_input(0, "Condition_1"))
        self.assertTrue(ast.verify_input(1, "Symptom_1"))
        self.assertTrue(ast.verify_input(2, "Sub_Symptom_1"))
        self.assertFalse(ast.verify_input(5, "Sub_Symptom_1"))
        self.assertFalse(ast.verify_input(1, "Condition"))

    def test_good_select_relevant_cond(self):
        self.assertEqual(ast.select_relevant_cond(self.correct_symptom, self.list_cond), ['Condition_1', 'Condition_2'])
        self.assertEqual(ast.select_relevant_cond(self.correct_symptom2, self.list_cond), ['Condition_1', 'Condition_2'])
        self.assertEqual(ast.select_relevant_cond(self.correct_symptom3, self.list_cond), ['Condition_1', 'Condition_2'])
        return

    def test_bad_select_relevant_cond(self):
        incorrect_symptom1 = "Symptom 10"
        incorrect_symptom2 = "Symptom 20"
        incorrect_symptom3 = 105
        incorrect_symptom4 = ["Symptom 1", "Symptom 2"]
        incorrect_symptom5 = ("Set 1", "Set 2")
        with self.assertRaises(networkx.exception.NetworkXError):
            ast.select_relevant_cond(self.incorrect_symptom, self.list_cond)
            ast.select_relevant_cond(incorrect_symptom1, self.list_cond)
            ast.select_relevant_cond(incorrect_symptom2, self.list_cond)
            ast.select_relevant_cond(incorrect_symptom3, self.list_cond)
            ast.select_relevant_cond(incorrect_symptom4, self.list_cond)
            ast.select_relevant_cond(incorrect_symptom5, self.list_cond)

    def test_good_select_relevant_symptoms(self):
        self.assertEqual(set(ast.select_relevant_symptoms(self.graph, self.correct_condition)), set(['Symptom_1', 'Symptom_2']))
        self.assertCountEqual(ast.select_relevant_symptoms(self.graph, self.correct_condition2), ['Symptom_1', 'Symptom_2'])
        return

    def test_bad_select_relevant_symptoms(self):
        incorrect_condition1 = "Condition 10"
        incorrect_condition2 = 250
        incorrect_condition3 = []
        incorrect_condition4 = ("Sponge1", "Sponge2")
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_symptoms(self.graph, self.incorrect_condition))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_symptoms(self.graph, incorrect_condition1))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_symptoms(self.graph, incorrect_condition2))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_symptoms(self.graph, incorrect_condition3))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_symptoms(self.graph, incorrect_condition4))

    def test_good_start_assessment(self):
        self.assertEqual(ast.start_assessment(self.correct_symptom), ['Sub1_symptom_1', 'Sub2_symptom_1'])
        self.assertEqual(ast.start_assessment(self.correct_symptom2), ['Sub1_symptom_2', 'Sub2_symptom_2'])
        return

    def test_bad_start_assessment(self):
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment("Bad Symptom"))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment(123))
        #self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment(["Symptom 1", "Symptom 2"]))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment("Condition_1"))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment())
        #self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment("Sub1_symptom_1"))
        #self.assertRaises(networkx.exception.NetworkXError, lambda: ast.start_assessment("Condition_1"))

    def evaluate(self):
        self.assertEqual((ast.evaluate(self.correct_symptom, self.correct_successors), self.user_sub_answers), [['Condition_1', 0.54], ['Condition_2', 0.47000000000000003]])
        self.assertEqual((ast.evaluate(self.correct_symptom2, self.correct_successors2), self.user_sub_answers), ['Condition_1', 0.272])
        return


if __name__ == '__main__':
    unittest.main()