# coding: utf-8

# get_ipython().run_line_magic('matplotlib', 'inline')
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel




# set structure -- defining relationships
state_network = BayesianModel([("Symptom_1", "Sub1_symptom_1"),
                               ("Symptom_1", "Sub2_symptom_1"),
                              ("Symptom_2", "Sub1_symptom_2"),
                               ("Symptom_2", "Sub2_symptom_2"),
                              ("Sub1_symptom_1", "Condition_1"),
                                ("Sub2_symptom_1", "Condition_2"),
                              ("Sub1_symptom_2", "Condition_1"),
                              ("Sub2_symptom_2", "Condition_2")])



# set up relationshipt - CPDs (Conditional Porbability Distribution)

Symptom1_cpd = TabularCPD(
                        variable = "Symptom_1",
                        variable_card = 2,
                        values = [[0.4,0.6]])


Symptom2_cpd = TabularCPD(
                        variable = "Symptom_2",
                        variable_card = 2,
                        values = [[0.3,0.7]])

Sub1_s1_cpd = TabularCPD(
                        variable = "Sub1_symptom_1",
                        variable_card = 2,
                        values = [[0.7,0.0],
                                 [0.3,1.0]],
                        evidence = ["Symptom_1"],
                        evidence_card = [2])

Sub2_s1_cpd = TabularCPD(
                        variable = "Sub2_symptom_1",
                        variable_card = 2,
                        values = [[0.5,0.0],
                                 [0.5,1.0]],
                        evidence = ["Symptom_1"],
                        evidence_card = [2])

Sub1_s2_cpd = TabularCPD(
                        variable = "Sub1_symptom_2",
                        variable_card = 2,
                        values = [[0.5,0.0],
                                 [0.5,1.0]],
                        evidence = ["Symptom_2"],
                        evidence_card = [2])
Sub2_s2_cpd = TabularCPD(
                        variable = "Sub2_symptom_2",
                        variable_card = 2,
                        values = [[0.5,0.0],
                                 [0.5,1.0]],
                        evidence = ["Symptom_2"],
                        evidence_card = [2])


Cond_1_cpd = TabularCPD(
                        variable = "Condition_1",
                        variable_card = 2,
                        values = [[0.8,0.4,0.7,0.1],
                                 [0.2,0.6,0.3,0.9]],
                        evidence = ["Sub1_symptom_1", "Sub1_symptom_2"],
                        evidence_card = [2,2])

Cond_2_cpd = TabularCPD(
                        variable = "Condition_2",
                        variable_card = 2,
                        values = [[0.7,0.5,0.8,0.2],
                                 [0.3,0.5,0.2,0.8]],
                        evidence = ["Sub2_symptom_1", "Sub2_symptom_2"],
                        evidence_card = [2,2])



state_network.add_cpds (Symptom1_cpd, 
                       Symptom2_cpd, 
                       Sub1_s1_cpd, 
                       Sub2_s1_cpd, 
                       Sub1_s2_cpd, 
                       Sub2_s2_cpd, 
                       Cond_1_cpd,
                       Cond_2_cpd
                       )

#list of all possible conditions in database
condition_list = ["Condition_1", "Condition_2", "Condition_3not"]



