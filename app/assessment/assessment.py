from graph import *
import networkx as nx
import pylab as plt
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
import re
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# def tbl_to_df():
# 	engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
# 	conditions = pd.read_sql("select * from conditions", engine)
# 	related_symptoms = pd.read_sql("select * from related_symptoms", engine)
# 	return conditions, related_symptoms
# print(state_network.get_cpds())

# network visual
# set structure -- defining relationships
# G_sympt = BayesianModel([("Symptom_1", "Sub1_symptom_1"),
#                                ("Symptom_1", "Sub2_symptom_1"),
#                               ("Symptom_2", "Sub1_symptom_2"),
#                                ("Symptom_2", "Sub2_symptom_2"),
#                               ("Sub1_symptom_1", "Condition_1"),
#                                 ("Sub2_symptom_1", "Condition_2"),
#                               ("Sub1_symptom_2", "Condition_1"),
#                               ("Sub2_symptom_2", "Condition_2")])

# values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 8)),
#                    columns=['Symptom_1', 'Symptom_2', 'Sub1_symptom_1', 'Sub1_symptom_2' ,'Sub2_symptom_1', 'Sub2_symptom_2', 'Condition_1', 'Condition_2'])
# # print(values)
# estimator = BayesianEstimator(G_sympt, values)
# x = estimator.get_parameters(prior_type='BDeu', equivalent_sample_size=5)
# for i,cpd in enumerate(x):
#     print(i, cpd.values)
#     G_sympt.add_cpds(cpd)

# print(estimator.estimate_cpd('Condition_2', prior_type="dirichlet", pseudo_counts=[1,2]))
# # inference on graph

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
def select_relevant_symptoms(graph, condition):
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

    #all condiitons to compare
    relev_conds = select_relevant_cond(symptom_init, condition_list) # condition_list is a global in graph.py
    llen = len(symp_list_val)
    #create evidence dict
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
        cond_scores_list.append(val_yes)

    index_max_prob = cond_scores_list.index(max(cond_scores_list))
    top_cond_candidate = relev_conds[index_max_prob]
    score_top = cond_scores_list[index_max_prob]

    condition_val_tuples = sorted(condition_val_tuples, key=lambda x: x[1], reverse=True)
    print(condition_val_tuples)

    # TODO: move this out
    rel_symptoms = select_relevant_symptoms(G_sympt, condition_val_tuples[0][0])
    print(rel_symptoms)

    print(top_cond_candidate, score_top)
    return condition_val_tuples

x = start_assessment("sympt_1")
res = evaluate("sympt_1", x, [1,0,1,1,0,0,1,1])

print(res)