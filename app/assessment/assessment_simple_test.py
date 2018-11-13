from graph import *
import networkx as nx
import pylab as plt
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
import re
from sqlalchemy import create_engine
import pandas as pd
import numpy as np



state_network2 = BayesianModel([("Symptom_1", "Sub1_symptom_1"),
                               ("Symptom_1", "Sub2_symptom_1"),
                              ("Symptom_2", "Sub1_symptom_2"),
                               ("Symptom_2", "Sub2_symptom_2"),
                              ("Sub1_symptom_1", "Condition_1"),
                                ("Sub2_symptom_1", "Condition_2"),
                              ("Sub1_symptom_2", "Condition_1"),
                              ("Sub2_symptom_2", "Condition_2")])



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



#  adding cpds to the graph
state_network2.add_cpds (Symptom1_cpd, 
                       Symptom2_cpd,
                       Sub1_s1_cpd, 
                       Sub2_s1_cpd, 
                       Sub1_s2_cpd, 
                       Sub2_s2_cpd,
                       Cond_1_cpd,
                       Cond_2_cpd
                       )



#  list of all possible condiitons in database
condition_list = ["Condition_1", "Condition_2", "Condition_3not"]



# inference on graph - alows for graph queries
network_infer = VariableElimination(state_network2)



# given symptom and all possible condiitons, outputs list of
# conditions with some degree of connection to this symptom
def select_relevant_cond(symptom, list_cond):
    relevant_cond = []
    trail_dic = state_network2.active_trail_nodes(symptom)
    trail_list = list(trail_dic[symptom])
    length = len(list_cond)
    for i in range(length):
        if list_cond[i] in trail_list:
            relevant_cond.append(list_cond[i])

    return relevant_cond



#  given condiiton and Baysian graph, imputs all the immediate parent of node condiiton
#  returns a list of sub-symptoms/symptoms immediately connected to the condition
def select_relevant_symptoms(graph, condition):
    ind = graph.local_independencies(condition)
    mystr = str(ind)
    wordList = mystr.replace("(","").replace(")","").replace(",","").split(" ")

    wordList.reverse()
    rel_symp = []
    for sub_symp in wordList:
        if sub_symp == '|':
            break;
        ind = graph.local_independencies(sub_symp)
        symp = str(ind).replace(",", "").replace(")","").split(" ")[-1]
        rel_symp.append(symp)

    return rel_symp



#  given initial symptom, outputs a list of all children (sub-symptoms) 
#  connected to the init_symptom node
def start_assessment(symptom_init):
    successors = list(state_network2.successors(symptom_init))

    return successors



#  given the name of the initial symptom (str), list of sub-symptoms to ini_symptom (list str),
#  and user answers (list int) (0 -- no, 1 -- yes), outputs 
def evaluate(symptom_init, successors, user_sub_answers):
    # starts with 'yes' for initial symptom
    symp_list_val = [1]
    symp_list_name = [symptom_init]
    for i, answer in enumerate(user_sub_answers):
        if answer == 'yes':
            symp_list_val.append(1)
            symp_list_name.append(successors[i])
        else:
            symp_list_val.append(0)
            symp_list_name.append(successors[i])

    # all condiitons to compare
    relev_conds = select_relevant_cond(symptom_init, condition_list) # condition_list is a global
    llen = len(symp_list_val)
    # creade evidence dict
    # e.g. {symptom:1}
    evidencee = {}
    cond_scores_list = []
    for k in range(llen):
        evidencee.update({symp_list_name[k]:symp_list_val[k]})
    len_rev_cond = len(relev_conds)
    condition_val_tuples = []
    for j in range(len_rev_cond):
        cond_prob = network_infer.query(variables = [relev_conds[j]],
                                    evidence = evidencee)
        val_yes = cond_prob[relev_conds[j]].values[1]
        condition_val_tuples.append([relev_conds[j], val_yes])
        cond_scores_list.append(val_yes)

    index_max_prob = cond_scores_list.index(max(cond_scores_list))
    top_cond_candidate = relev_conds[index_max_prob]
    score_top = cond_scores_list[index_max_prob]

    condition_val_tuples = sorted(condition_val_tuples, key=lambda x: x[1], reverse=True)

    rel_symptoms = select_relevant_symptoms(state_network2, condition_val_tuples[0][0])


    print(top_cond_candidate, score_top)
    return condition_val_tuples




x = start_assessment("Symptom_1")
evaluate("Symptom_1", x, [1,0])
