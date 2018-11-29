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
# from users import *


# Extracts data from DynamoDB. 3 tables: Conditions, Related symptoms, sub symptom names
def tbl_to_df():
    engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    conditions = pd.read_sql("select * from conditions", engine)
    related_symptoms = pd.read_sql("select * from related_symptoms", engine)
    sub_symptom_names = pd.read_sql("select * from sub_symptom_names", engine)
    return conditions, related_symptoms, sub_symptom_names

df_cond, df_related_symptoms, df_sub_symptom_names = tbl_to_df()

def tbl_to_df_sympt_id(sympt_id):
    engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    related_symptoms = pd.read_sql("select * from related_symptoms where sympt_id = '" + sympt_id + "'", engine)
    return related_symptoms

df_related_symptoms_sympt_1 = tbl_to_df_sympt_id("sympt_1")

# Create Bayesian Model

def load_graph_sympt_id(df_cond, df_related_symptoms, sympt_id):
    G = BayesianModel()
    sub_symptom_list = []
    condition_list = set()
    for i, row in df_related_symptoms.iterrows():

        symptom_id = str(row[0])
        if (symptom_id == sympt_id):
            for j, col in row.iteritems():
                sub_symptom_id = str(j)
                if sub_symptom_id[:8]== "sub_symp":
                    if col != 0:
                        G.add_edge(symptom_id, sub_symptom_id)
                        sub_symptom_list.append(sub_symptom_id)


    for i, row in df_cond.iterrows():
        cond_id = str(row[0])
        for j, col in row.iteritems():
            if col != 0.0:
                sub_symptom_id = str(j)
                # print(symptom_id, cond_id)
                if (sub_symptom_id in sub_symptom_list):
                    G.add_edge(sub_symptom_id, cond_id)
                    condition_list.add(cond_id)
    condition_list = list(condition_list)
    return G, sub_symptom_list, condition_list

G_sympt_1, sympt_1_sub_list, condition_list = load_graph_sympt_id(df_cond, df_related_symptoms, "sympt_1")

print(len(sympt_1_sub_list))
print(sympt_1_sub_list)
print(condition_list)

num_conditions = df_cond.shape[0]
num_symptoms = df_related_symptoms.shape[0]
num_sub_symptoms = df_sub_symptom_names.shape[0]

all_symptoms = list(df_related_symptoms['sympt_id'])
all_conditions = list(df_cond['cond_id'])
all_sub_symptoms = list(df_sub_symptom_names['sub_sympt_id'])


def create_all_symptom_graphs(df_cond, df_related_symptoms):
    d = {} # symptom_id: [Graph, subsymptoms, conditions]
    for sympt_id in all_symptoms:
        print(sympt_id)
        G, sub_symptom_list, condition_list = load_graph_sympt_id(df_cond, df_related_symptoms, sympt_id)
        d[sympt_id] = [G, sub_symptom_list, condition_list]
    return d 

graph_dict = create_all_symptom_graphs(df_cond, df_related_symptoms)
print(graph_dict)


def load_cpds():
    for sympt_id in graph_dict:
        print(sympt_id)
        G_sympt = graph_dict[sympt_id][0]
        data = pd.DataFrame(np.random.randint(low=0, high=2, size=(100, len(G_sympt.nodes))),
                   columns= G_sympt.nodes)
        G_sympt.fit(data, estimator=BayesianEstimator, prior_type="BDeu")

load_cpds()

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
            sub_symptom_id = str(j)
            if sub_symptom_id[:8]== "sub_symp":
                if col != 0.0:
                    G.add_edge(sympt_id, sub_symptom_id)
    return G

G = load_graph(df_cond, df_related_symptoms)

# All the nodes in the graph (157 nodes)
gnodes = G.nodes

print(len(G.edges))

data = pd.DataFrame(np.random.randint(low=0, high=2, size=(10, len(gnodes))),
                   columns= gnodes)
data_sympt_1 = pd.DataFrame(np.random.randint(low=0, high=2, size=(300, len(G_sympt_1.nodes))),
                   columns= G_sympt_1.nodes)
# G.fit(data)

# print(values2)
estimator2 = BayesianEstimator(G, data)
estimator_sympt_1 = BayesianEstimator(G_sympt_1, data_sympt_1)


# for i in range(1, num_sub_symptoms + 1):
#     print(i)
#     cpd_sub = estimator2.estimate_cpd('sub_sympt_' + str(i), prior_type="BDeu")
#     G.add_cpds(cpd_sub)
#     if i <= num_symptoms:
#         cpd_symp = estimator2.estimate_cpd('sympt_' + str(i), prior_type="BDeu")
#         G.add_cpds(cpd_symp)


# print("done population symptoms and subsymptoms cpds")
# print(G.get_cpds())






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
# G_sympt_1.fit(data_sympt_1, estimator=BayesianEstimator, prior_type="BDeu")
# print(len(G_sympt_1.get_cpds()))
# estimator_sympt_1 = BayesianEstimator(G_sympt_1, data_sympt_1)
# G_sympt_1_parameters = estimator_sympt_1.get_parameters(prior_type='BDeu', equivalent_sample_size=5)

# for i,cpd in enumerate(G_sympt_1_parameters):
#   print(i, cpd.values, cpd)






