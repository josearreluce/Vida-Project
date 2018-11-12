from graph import *
import networkx as nx
import pylab as plt
from pgmpy.inference import VariableElimination

# print(state_network.get_cpds())

# network visual
nx.draw(state_network, with_labels=True)
plt.show()

# inference on graph
network_infer = VariableElimination(state_network)

# given symptom and all possible condiitons, outputs list of
# conditions with some degree of connection to this symptom
def select_relevant_cond(symptom, list_cond):
    relevant_cond = []
    trail_dic = state_network.active_trail_nodes(symptom)
    trail_list = list(trail_dic[symptom])
    length = len(list_cond)
    for i in range(length):
        if list_cond[i] in trail_list:
            relevant_cond.append(list_cond[i])
    return relevant_cond



# 0 -- yes, 1 -- no
# what happens when user mystypes symptom
def assessment():
    #starts with 'yes' for initial symptom
    symptom_init = input("What symptom is bothering you the most   ")
    symp_list_val = [0]
    symp_list_name = [symptom_init]
    if state_network.has_node(symptom_init) != True:
        print("this symptom not in database")
    else:
        # subsymptoms
        successors = list(state_network.successors(symptom_init))
        ls = len(successors)
        for i in range(ls):
            sub_s = successors[i]
            x = input("Do you have, {}   ".format(sub_s))
            if x == 'yes':
                symp_list_val.append(0)
                symp_list_name.append(successors[i])
            else:
                symp_list_val.append(1)
                symp_list_name.append(successors[i])
        #all condiitons to compare
        relev_conds = select_relevant_cond(symptom_init, condition_list)
        llen = len(symp_list_val)
        #creade evidence dict
        evidencee = {}
        cond_scores_list = []
        for k in range(llen):
            evidencee.update({symp_list_name[k]:symp_list_val[k]})   
        len_rev_cond = len(relev_conds)
        for j in range(len_rev_cond):
            cond_prob = network_infer.query(variables = [relev_conds[j]],
                                        evidence = evidencee)
            val_yes = cond_prob[relev_conds[j]].values[0]
            cond_scores_list.append(val_yes)
        
        index_max_prob = cond_scores_list.index(max(cond_scores_list))
        top_cond_candidate = relev_conds[index_max_prob]
        score_top = cond_scores_list[index_max_prob]
        
        print(top_cond_candidate, score_top)
           

assessment() 