import unittest
import sys
import networkx
sys.path.append('../assessment')
sys.path.append('../src')
sys.path.append('../../')
import assessment_simple_test as ast
from users import  *
from app.models import UserSession
import assessment as ass

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
        self.assertEqual(ast.select_relevant_cond(self.correct_symptom3, self.list_cond), [])

    def test_bad_select_relevant_cond(self):
        incorrect_symptom1 = "Symptom 10"
        incorrect_symptom2 = "Symptom 20"
        incorrect_symptom3 = 105
        incorrect_symptom4 = ["Symptom 1", "Symptom 2"]
        incorrect_symptom5 = ("Set 1", "Set 2")
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_cond(self.incorrect_symptom, self.list_cond))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_cond(incorrect_symptom1, self.list_cond))
        self.assertRaises(networkx.exception.NetworkXError, lambda: ast.select_relevant_cond(incorrect_symptom2, self.list_cond))
        #self.assertEquals(ast.select_relevant_cond(incorrect_symptom3, self.list_cond), [])
        self.assertRaises(TypeError, lambda: ast.select_relevant_cond(incorrect_symptom3, self.list_cond))
        self.assertEquals(ast.select_relevant_cond(incorrect_symptom4, self.list_cond), [])
        self.assertEquals(ast.select_relevant_cond(incorrect_symptom5, self.list_cond), [])

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
        self.assertRaises(TypeError, lambda: ast.select_relevant_symptoms(self.graph, incorrect_condition2))

        self.assertEquals(ast.select_relevant_symptoms(self.graph, incorrect_condition3), [])
        self.assertEquals(ast.select_relevant_symptoms(self.graph, incorrect_condition3), [])
        self.assertEquals(ast.select_relevant_symptoms(self.graph, incorrect_condition4), [])

    def test_good_start_assessment(self):
        self.assertEqual(ast.start_assessment(self.correct_symptom), ['Sub1_symptom_1', 'Sub2_symptom_1'])
        self.assertEqual(ast.start_assessment(self.correct_symptom2), ['Sub1_symptom_2', 'Sub2_symptom_2'])
        return

    def test_bad_start_assessment(self):
        self.assertRaises(TypeError, lambda: ast.start_assessment(123))
        self.assertRaises(TypeError, lambda: ast.start_assessment())

        self.assertEquals(ast.start_assessment(["Symptom 1", "Symptom 2"]), [])
        self.assertEquals(ast.start_assessment("Sub1_symptom_1"), [])
        self.assertEquals(ast.start_assessment("Condition_1"), [])

        self.assertEquals(ast.start_assessment("Bad Symptom"), [])


    def test_evaluate(self):
        print(ast.evaluate(self.correct_symptom, self.correct_successors, self.user_sub_answers))
        self.assertEqual([[x[0], round(x[1], 2)] for x in ast.evaluate(self.correct_symptom, self.correct_successors, self.user_sub_answers)], [['Condition_1', 0.54], ['Condition_2', 0.47]])
        self.assertEqual([[x[0], round(x[1], 3)] for x in ast.evaluate(self.correct_symptom2, self.correct_successors2, self.user_sub_answers)],  [['Condition_1', 0.272], ['Condition_2', 0.22]])
        return
"""
    Unit Test Cases used for testing the functions used by the assessment algorithm
    to take into account User Profile information when outputting conditions with
    probabilities.
"""
class TestAssessmentWithUser(unittest.TestCase):
    def setUp(self):

        # Setup the testcase
        self.account_info = AccountInfo("bbjacob", "bru123321")
        self.basic_info = BasicInfo(22, 1)  # sex 1-male, 2-female
        self.personal_info = PersonalInfo(185, 81)  # cm, kg
        self.health_back = HealthBackground(0, 0, 0)  # 0-no, 1-yes, 2-not responded
        self.user = UserSession.query.filter_by(username="test_username").first()
        
        self.account_info2 = AccountInfo("bbjacob", "bru123321")
        self.basic_info2 = BasicInfo(50, 2)
        self.personal_info2 = PersonalInfo(185, 80)
        self.health_back2 = HealthBackground(0, 0, 0)
        self.user2 = User(self.account_info2, self.basic_info2, self.personal_info2, self.health_back2)

        # Personal feature "correct" answers
        self.cvt1 = [['cond_1', 0.5853757342515697], ['cond_2', 0.41462426574843025]]
        self.cvt2 = [['cond_3', 0.9405940594059405], ['cond_10', 0.0594059405940594]]
        self.cvt3 = [['cond_5', 0.5], ['cond_7', 0.3], ['cond_10', 0.2]]
        self.cvt_bad = 0
        
        self.cvt_change = [['cond_1', 0.5754345210934583], ['cond_2', 0.4245654789065417]]

        # Conditions, Symptoms, and Subsymptoms

        # Personal feature initial inputs
        self.cvt_prior1 = [['cond_1', 0.47752808988764045], ['cond_2', 0.40588235294117647]]
        self.cvt_prior2 = [['cond_3', 0.95], ['cond_10', 0.05]]
        self.cvt_prior3 = [['cond_5', 0.5], ['cond_7', 0.3], ['cond_10', 0.2]]
        self.cvt_bad1 = [['cond_1', 0.4], ['cond_2', -0.4]]  # Bad input
        self.cvt_bad2 = [['cond_1', 0], ['cond_2', 1]]  # Bad input - should never have a "0"

        self.time = 10

        # Graphical Setup
        self.df_cond, self.df_related_symptoms, self.sss = ass.tbl_to_df()
        self.graph = ass.load_graph(self.df_cond, self.df_related_symptoms)

        self.nodes = 157
        self.edges = 293

        # CPDs Setup
        self.data = ass.load_cpds()

    # Test that the probabilities for the conditions change when personal features are applied.
    def test_apply_user_features(self):
        print(self.user)
        self.assertEqual(ass.apply_personal_features(self.user, self.cvt_prior1, self.time), self.cvt1)
        self.assertEqual(ass.apply_personal_features(self.user, self.cvt_prior2, self.time), self.cvt2)
        self.assertEqual(ass.apply_personal_features(self.user, self.cvt_prior3, self.time), self.cvt3)

        self.assertEqual(ass.apply_personal_features(self.user, self.cvt_bad1, self.time), self.cvt_bad)
        self.assertEqual(ass.apply_personal_features(self.user, self.cvt_bad2, self.time), self.cvt_bad)

        self.assertEqual(ass.apply_personal_features(self.user2, self.cvt_prior1, self.time), self.cvt_change)
        self.assertNotEqual(ass.apply_personal_features(self.user2, self.cvt_prior1, self.time), self.cvt1)


    def test_load_graph(self):  # No real possibility for a bad input - this is what creates the entire graph.
        self.assertEqual(len(self.graph.nodes), self.nodes)
        self.assertEqual(len(self.graph.edges), self.edges)


    def test_load_cpds(self):
        self.assertEqual(self.data.size, 1545)  # Acts like a helper function - this just asserts that the size is correct


if __name__ == '__main__':
    unittest.main()
