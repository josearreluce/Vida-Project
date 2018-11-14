# coding: utf-8

# get_ipython().run_line_magic('matplotlib', 'inline')
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
import numpy as np
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
import pandas as pd
from sqlalchemy import create_engine
import re

import networkx as nx
import pylab as plt



def tbl_to_df():
    engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    conditions = pd.read_sql("select * from conditions", engine)
    related_symptoms = pd.read_sql("select * from related_symptoms", engine)
    return conditions, related_symptoms


print("in graph.py")

df_cond, df_related_symptoms = tbl_to_df()

print(df_cond)
# print(df_related_symptoms)

symptom_id = ""
cond_id = ""

G = BayesianModel()
symptoms = list(df_cond.columns.values)
print(df_cond.columns[1])
# print(df_cond[['cond_id']])
cond_id_list = []
print(symptoms)
# index 4 = symptom 1
# how it looks [u'cond_id', u'name', u'desc', u'sex', u'sympt_1',u'sympt_2']
for i, row in df_cond.iterrows():

    cond_id = "cond_" + str(i + 1)
    cond_id_list.append(cond_id)
    for j, col in row.iteritems():
        if col == 1:
            symptom_id = str(j)
            # print(symptom_id, cond_id)
            G.add_edge(symptom_id, cond_id)


print(cond_id_list)
print(len(G.nodes))

nx.draw(G, with_labels=True)
plt.show()


print(len(symptoms))
print(len(cond_id_list))
str_symptoms = [str(x) for x in symptoms[4::]]
print(str_symptoms)

# values2 = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 129)),
#                    columns= str_symptoms + cond_id_list)

combined = str_symptoms + cond_id_list
print(combined)

gnodes = G.nodes
#make it same format table
#130 originally
values2 = pd.DataFrame(np.random.randint(low=0, high=2, size=(12, 130)),
                   columns= gnodes)

print(values2)
estimator2 = BayesianEstimator(G, values2)

# cpd_C = estimator2.estimate_cpd('cond_1', prior_type="dirichlet", pseudo_counts=[1, 2])
# print(cpd_C)

params = estimator2.get_parameters(prior_type='BDeu', equivalent_sample_size=5)
for i,cpd in enumerate(params):
    # print(i, cpd.values)
    G.add_cpds(cpd)




# print(estimator2.estimate_cpd('cond_1', prior_type="dirichlet", pseudo_counts=[1,2]))


# set structure -- defining relationships
state_network = BayesianModel([("Symptom_1", "Sub1_symptom_1"),
                               ("Symptom_1", "Sub2_symptom_1"),
                              ("Symptom_2", "Sub1_symptom_2"),
                               ("Symptom_2", "Sub2_symptom_2"),
                              ("Sub1_symptom_1", "Condition_1"),
                                ("Sub2_symptom_1", "Condition_2"),
                              ("Sub1_symptom_2", "Condition_1"),
                              ("Sub2_symptom_2", "Condition_2")])



values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 8)),
                   columns=['Symptom_1', 'Symptom_2', 'Sub1_symptom_1', 'Sub1_symptom_2' ,'Sub2_symptom_1', 'Sub2_symptom_2', 'Condition_1', 'Condition_2'])
# print(values)
estimator = BayesianEstimator(state_network, values)
x = estimator.get_parameters(prior_type='BDeu', equivalent_sample_size=5)
for i,cpd in enumerate(x):
    # print(i, cpd.values)
    state_network.add_cpds(cpd)

# print(estimator.estimate_cpd('Condition_2', prior_type="dirichlet", pseudo_counts=[1,2]))


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



# state_network.add_cpds (Symptom1_cpd, 
#                        Symptom2_cpd, 
#                        Sub1_s1_cpd, 
#                        Sub2_s1_cpd, 
#                        Sub1_s2_cpd, 
#                        Sub2_s2_cpd, 
#                        Cond_1_cpd,
#                        Cond_2_cpd
#                        )

#list of all possible conditions in database
condition_list = ["Condition_1", "Condition_2", "Condition_3not"]



