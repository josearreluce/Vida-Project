from graph import *
import networkx as nx
import pylab as plt
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
import re
from sqlalchemy import create_engine
import pandas as pd
import numpy as np


# network_infer = VariableElimination(G_sympt_1)
# given symptom and all possible condiitons, outputs list of
# conditions with some degree of connection to this symptom
def select_relevant_cond(symptom, list_cond):
    G_sympt = graph_dict[symptom][0]
    relevant_cond = []
    trail_dic = G_sympt.active_trail_nodes(symptom)
    trail_list = list(trail_dic[symptom])
    length = len(list_cond)
    for i in range(length):
        if list_cond[i] in trail_list:
            relevant_cond.append(list_cond[i])
    return relevant_cond


#given condition, find all related symptoms
def select_relevant_symptoms(graph, condition, symptom_init):
    ind = graph.local_independencies(condition)
    mystr = str(ind)
    wordList = mystr.replace("(","").replace(")","").replace(",","").split(" ")

    wordList.reverse()
    rel_symp = set()
    for sub_symp in wordList:
        if sub_symp == '|':
            break;
        ind = graph.local_independencies(sub_symp)
        symp = str(ind).replace(",", "").replace(")","").split(" ")[-1]
        rel_symp.add(symp)
    if symptom_init in rel_symp:
        rel_symp.remove(symptom_init)
    return list(rel_symp)



# 0 -- no, 1 -- yes
# what happens when user mystypes symptom
def start_assessment(symptom_init):
    G_sympt = graph_dict[symptom_init][0]
    successors = list(G_sympt.successors(symptom_init))

    return successors


def evaluate(symptom_init, successors, user_sub_answers):
    #starts with 'yes' for initial symptom
    G_sympt = graph_dict[symptom_init][0]
    condition_list = graph_dict[symptom_init][2]
    network_infer = VariableElimination(G_sympt)

    symp_list_val = [1]
    symp_list_name = [symptom_init]
    for i,answer in enumerate(user_sub_answers):
        if answer == 'yes':
            symp_list_val.append(1)
            symp_list_name.append(successors[i])
        else:
            symp_list_val.append(0)
            symp_list_name.append(successors[i])

    # all condiitons to compare
    # condition_list is all the conditions reachable via symptom_init
    relev_conds = select_relevant_cond(symptom_init, condition_list) 
    llen = len(symp_list_val)

    # create evidence dict
    # e.g. {symptom:yes}
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

    condition_val_tuples = sorted(condition_val_tuples, key=lambda x: x[1], reverse=True)

    # print(top_cond_candidate, score_top)
    return condition_val_tuples

def followup(initial_evaluate, symptom_init):

    # find relevant symptoms given the top probabilistic condition 
    rel_symptoms = select_relevant_symptoms(total_G, initial_evaluate[0][0], symptom_init)

    successors_list = []
    for sympt_id in rel_symptoms:
        successors = start_assessment(sympt_id)
        successors_list.append(successors)

    return rel_symptoms, successors_list 

# list of symptoms, list of successors, list of user_sub_answers. (1D, 2D, 2D)
# returns updated probabilty on the top probabilistic condition in the initial evaluate
def followup2(rel_symptoms, successors_list, user_sub_answers, cond_id):

    condition_val_tuples_matrix = []
    for i,sympt_id in enumerate(rel_symptoms):
        evaluated = evaluate(sympt_id, successors_list[i], user_sub_answers[i])
        condition_val_tuples_matrix.append(evaluated)

    cond_id_values = []
    for cond_val_tuples_list in condition_val_tuples_matrix:
        for cond, val in cond_val_tuples_list:
            if cond == cond_id:
                cond_id_values.append(val)
    average = sum(cond_id_values) / (len(cond_id_values) * 1.0)

    return [cond_id, average]



# Testing Examples
x = start_assessment("sympt_1")
res = evaluate("sympt_1", x, [1,0,1,1,0,0,1,1])
print(res)

x3 = start_assessment("sympt_27")
res3 = evaluate("sympt_27", x3, [0])
print(res3)

x4 = start_assessment("sympt_8")
res4 = evaluate("sympt_8", x4, [0, 0, 1, 1])
print(res4)

x2 = start_assessment("sympt_12")
res2 = evaluate("sympt_12", x2, [1,1])
print(res2)

rel_symptoms, successors_list = followup(res2, "sympt_12")
print(rel_symptoms)
print(successors_list)

fake_user_sub = []
for s_list in successors_list:
    new = []
    for sub in s_list:
        new.append(np.random.randint(low=0, high=2))
    fake_user_sub.append(new)

fup2 = followup2(rel_symptoms, successors_list, fake_user_sub, res2[0][0])
print(fup2)