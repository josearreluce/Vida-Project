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
# sys.path.append('../src')
# from users import *
sys.path.append('../../')
from app.src.users import *
from app import models
from app.models import DatabaseConnection, UserSession


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


# Create Bayesian Model given symptom id
def load_graph_sympt_id(df_cond, df_related_symptoms, sympt_id):
    G = BayesianModel()
    sub_symptom_list = []
    condition_list = set()

    # Go through related symptoms table and add edges (symptom -> sub symptom)
    for i, row in df_related_symptoms.iterrows():

        symptom_id = str(row[0])
        if (symptom_id == sympt_id):
            for j, col in row.iteritems():
                sub_symptom_id = str(j)
                if sub_symptom_id[:8]== "sub_symp":
                    if col != 0:
                        G.add_edge(symptom_id, sub_symptom_id)
                        sub_symptom_list.append(sub_symptom_id)

    # Go through conditions table and add edges (sub symptom -> condition)
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

num_conditions = df_cond.shape[0]
num_symptoms = df_related_symptoms.shape[0]
num_sub_symptoms = df_sub_symptom_names.shape[0]

all_symptoms = list(df_related_symptoms['sympt_id'])
all_conditions = list(df_cond['cond_id'])
all_sub_symptoms = list(df_sub_symptom_names['sub_sympt_id'])


def create_all_symptom_graphs(df_cond, df_related_symptoms):
    d = {} # symptom_id: [Graph, subsymptoms, conditions]
    for sympt_id in all_symptoms:
        G, sub_symptom_list, condition_list = load_graph_sympt_id(df_cond, df_related_symptoms, sympt_id)
        d[sympt_id] = [G, sub_symptom_list, condition_list]
    return d 

graph_dict = create_all_symptom_graphs(df_cond, df_related_symptoms)

def load_cpds():
    for sympt_id in graph_dict:
        G_sympt = graph_dict[sympt_id][0]
        data = pd.DataFrame(np.random.randint(low=0, high=2, size=(100, len(G_sympt.nodes))),
                   columns= G_sympt.nodes)
        G_sympt.fit(data, estimator=BayesianEstimator, prior_type="BDeu")
    print("loaded cpds")

load_cpds()











# Makes giant graph for all nodes 
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

total_G = load_graph(df_cond, df_related_symptoms)


# Compute and load all cpds for total graph. Takes a long time
def load_total_cpds():
    # All the nodes in the graph (157 nodes)
    gnodes = total_G.nodes

    data = pd.DataFrame(np.random.randint(low=0, high=2, size=(100, len(gnodes))),
                       columns= gnodes)
    # Option 1 of fitting cpds
    estimator = BayesianEstimator(total_G, data)
    p = estimator.get_parameters(prior_type='BDeu', equivalent_sample_size=5)
    for i,cpd in enumerate(p):
        total_G.add_cpds(cpd)




    # Option 2 of fitting cpds
    for i in range(1, num_sub_symptoms + 1):
        cpd_sub = estimator.estimate_cpd('sub_sympt_' + str(i), prior_type="BDeu")
        total_G.add_cpds(cpd_sub)
        if i <= num_symptoms:
            cpd_symp = estimator.estimate_cpd('sympt_' + str(i), prior_type="BDeu")
            total_G.add_cpds(cpd_symp)


    print("done population symptoms and subsymptoms cpds")
    print(total_G.get_cpds())

    # this is the time cruncher.
    for i in range(1, num_conditions + 1):
        cpd_cond = estimator.estimate_cpd('cond_' + str(i), prior_type="BDeu")
        total_G.add_cpds(cpd_cond)

#load_total_cpds()

def dbUsertoUser(userschema):

    # Account Info
    acc_info = AccountInfo(userschema.username, userschema.pswd)

    # Basic Info
    basic_info = BasicInfo(userschema.age, userschema.sex)

    # Personal Info
    personal_info = PersonalInfo(userschema.height, userschema.weight)

    # Health Background
    blood_pressure = (userschema.blood_pressure_low, userschema.blood_pressure_high)
    health_background = HealthBackground(userschema.smoker, blood_pressure, userschema.diabetes)

    return User(acc_info, basic_info, personal_info, health_background)