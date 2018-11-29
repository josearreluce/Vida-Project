# coding: utf-8

# get_ipython().run_line_magic('matplotlib', 'inline')
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel

from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
import networkx as nx
import pylab as plt
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
import re
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import sys
sys.path.append('../src')
from users import *


# Extracts data from DynamoDB. 3 tables: Conditions, Related symptoms, sub symptom names
def tbl_to_df():
    engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    conditions = pd.read_sql("select * from conditions", engine)
    related_symptoms = pd.read_sql("select * from related_symptoms", engine)
    sub_symptom_names = pd.read_sql("select * from sub_symptom_names", engine)
    return conditions, related_symptoms, sub_symptom_names

df_cond, df_related_symptoms, df_sub_symptom_names = tbl_to_df()

# def tbl_to_df_sympt_id(sympt_id):
#     engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
#     related_symptoms = pd.read_sql("select * from related_symptoms where sympt_id = '" + sympt_id + "'", engine)
#     return related_symptoms

# df_related_symptoms_sympt_1 = tbl_to_df_sympt_id("sympt_1")

# # Create Bayesian Model

# def load_graph(df_cond, df_related_symptoms, sympt_id):
#     G = BayesianModel()
#     sub_symptom_list = []
#     for i, row in df_related_symptoms.iterrows():

#         sympt_id = row[0]
#         for j, col in row.iteritems():
#             sub_sympt_id = str(j)
#             if sub_sympt_id[:8]== "sub_symp":
#                 if col != 0:
#                     G.add_edge(sympt_id, sub_sympt_id)
#                     sub_symptom_list.append(sub_sympt_id)

#     return G

# G_symp1 = BayesianModel()

num_conditions = df_cond.shape[0]
num_symptoms = df_related_symptoms.shape[0]
num_sub_symptoms = df_sub_symptom_names.shape[0]

def load_graph(df_cond, df_related_symptoms):
    G = BayesianModel()
    # Go through conditions table and add edges (sub symptom -> condition)
    for i, row in df_cond.iterrows():

        cond_id = str(row[0])
        for j, col in row.iteritems():
            if col != 0.0:
                sub_symptom_id = str(j)
                # print(symptom_id, cond_id)
                if (sub_symptom_id[:8] == 'sub_symp'):
                    G.add_edge(sub_symptom_id, cond_id)
                    
    # Go through related symptoms table and add edges (symptom -> sub symptom)
    for i, row in df_related_symptoms.iterrows():

        sympt_id = str(row[0])
        for j, col in row.iteritems():
            sub_sympt_id = str(j)
            if sub_sympt_id[:8]== "sub_symp":
                if col != 0:
                    G.add_edge(sympt_id, sub_sympt_id)
    return G

G = load_graph(df_cond, df_related_symptoms)

# All the nodes in the graph (157 nodes)
gnodes = G.nodes

print(len(G.edges))

data = pd.DataFrame(np.random.randint(low=0, high=2, size=(10, len(gnodes))),
                   columns= gnodes)
# G.fit(data)

# print(values2)
estimator2 = BayesianEstimator(G, data)

# cpd_cond_1 = estimator2.estimate_cpd('sympt_1', prior_type="BDeu", equivalent_sample_size=10)
# print(cpd_cond_1.values)
# print(1)

# cpd_cond_2 = estimator2.estimate_cpd('sympt_2', prior_type="BDeu", equivalent_sample_size=10)
# print(cpd_cond_2.values)
# print(2)

# cpd_cond_3 = estimator2.estimate_cpd('sub_sympt_3', prior_type="BDeu", equivalent_sample_size=10)
# print(cpd_cond_3.values)
# print(3)

cpd_cond_4 = estimator2.estimate_cpd('cond_4', prior_type="BDeu", equivalent_sample_size=10)
print(cpd_cond_4)

cpd_cond_5 = estimator2.estimate_cpd('cond_5', prior_type="BDeu", equivalent_sample_size=10)
print(cpd_cond_5)

cpd_cond_6 = estimator2.estimate_cpd('cond_6', prior_type="BDeu", equivalent_sample_size=10)
print(cpd_cond_6)

num_sub_symptoms = 110
num_symptoms = 35
for i in range(1, int(num_sub_symptoms/2)):
    print(i)
    cpd_sub = estimator2.estimate_cpd('sub_sympt_' + str(i), prior_type="BDeu")
    G.add_cpds(cpd_sub)
    if i <= num_symptoms:
        cpd_symp = estimator2.estimate_cpd('sympt_' + str(i), prior_type="BDeu")
        G.add_cpds(cpd_symp)

print("first batch done")
for i in range(int(num_sub_symptoms/2), num_sub_symptoms+1):
    print(i)
    cpd_sub = estimator2.estimate_cpd('sub_sympt_' + str(i), prior_type="BDeu")
    print(cpd_sub.values)
    # G.add_cpds(cpd_sub)

print("done population symptoms and subsymptoms cpds")






# params = estimator2.get_parameters(prior_type='BDeu', equivalent_sample_size=2)
# for i,cpd in enumerate(params):
#     print(i, cpd.values)
#     if i == 2:
#         break;
#     G.add_cpds(cpd)

# values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 4)),
#                       columns=['A', 'B', 'C', 'D'])
# model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D')])
# estimator = BayesianEstimator(model, values)
# p = estimator.get_parameters(prior_type='BDeu', equivalent_sample_size=5)
# for i,cpd in enumerate(p):
#     print(i, cpd.values, cpd)
    

# G.fit(data, estimator=BayesianEstimator, prior_type="BDeu")


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



