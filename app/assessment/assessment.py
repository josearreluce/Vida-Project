from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
from sqlalchemy import create_engine
import pandas as pd
import numpy as np




def get_name_from_id(id, df):
    index = df[df.columns[0]][df[df.columns[0]]==id].index[0]
    return df.iloc[index]['name']

def get_id_from_name(name, df):
    index = df['name'][df['name']==name].index[0]
    return df.iloc[index][df.columns[0]]


# Extracts data from DynamoDB. 3 tables: Conditions, Related symptoms, sub symptom names
def tbl_to_df():
    engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    conditions = pd.read_sql("select * from conditions", engine)
    related_symptoms = pd.read_sql("select * from related_symptoms", engine)
    sub_symptom_names = pd.read_sql("select * from sub_symptom_names", engine)
    return conditions, related_symptoms, sub_symptom_names

df_cond, df_related_symptoms, df_sub_symptom_names = tbl_to_df()


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



def get_all_symptoms():
    temp_id = list(df_related_symptoms['sympt_id'])
    res =[]
    for id1 in temp_id:

        name = get_name_from_id(id1, df_related_symptoms)

        res.append(name)
    return res


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
        data = pd.DataFrame(np.random.randint(low=0, high=2, size=(103, len(G_sympt.nodes))),
                   columns= G_sympt.nodes)

        graph_dict[sympt_id][0].fit(data, estimator=BayesianEstimator, prior_type="BDeu")

    return data

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

    # this is the time cruncher.
    for i in range(1, num_conditions + 1):
        cpd_cond = estimator.estimate_cpd('cond_' + str(i), prior_type="BDeu")
        total_G.add_cpds(cpd_cond)

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



#returns successors for inital symptom
def start_assessment(symptom_init):
    symptom_init = get_id_from_name(symptom_init, df_related_symptoms)
    G_sympt = graph_dict[symptom_init][0]
    successors = list(G_sympt.successors(symptom_init))

    successors_names = []
    for sub_id in successors:
        successors_names.append(get_name_from_id(sub_id, df_sub_symptom_names))

    return successors_names

def tbl_to_df_cond_id(cond_id):
    engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    info = pd.read_sql("select * from conditions where cond_id = '" + cond_id + "'", engine)
    return info

#given panda dataframe of condition extracts informtion of condition
def extract_from_cond(info):
    sex_age_time = []
    sex = [info.sex[0]]
    age_max = info.age_max[0]
    age_min = info.age_min[0]
    time_min = info.time_min[0]
    time_max = info.time_max[0]
    age = [age_min, age_max]
    time = [time_min, time_max]
    sex_age_time = sex_age_time + sex + age + time
    return sex_age_time

#given user extracts user information (sex and age)
def extract_from_user(user):
    sex_age = []
    sex = [user.sex]
    age = [user.age]
    sex_age = sex_age + sex + age
    return sex_age

#sex, age, time
def check_cvts(condition_val_tuples):  #The only requirement is that they need to be non-negative
    for condition_tuple in condition_val_tuples:
        if condition_tuple[1] < 0:
            return False


#given user, condition val tuples, and time variable applies personal feature to 
#the condition val tuples and returns new condition val tuples
def apply_personal_features(user, condition_val_tuples, time_first_symptom):
    print("Entering apply personal features __________")
    if time_first_symptom < 0:
        return 0  # Impossible.

    if check_cvts(condition_val_tuples) is False:  # Non-negative required
        return 0

    array_new = []  # an array for normalization

    new_cond_val_tuples = condition_val_tuples
    user_info = extract_from_user(user)
    u_sex = user_info[0]
    # print("SEX__", u_sex)
    u_age = user_info[1]
    time = time_first_symptom
    # print("HERE_1")
    # print("condition val tuples", condition_val_tuples)

    for condition_tuple in new_cond_val_tuples:
        # print("HERE_2")
        # print("conditon_t",condition_tuple)
        # print("new_cond_tuples", new_cond_val_tuples)
        cond_id = condition_tuple[0]
        info = tbl_to_df_cond_id(cond_id)
        cond_info_sex_age_time = extract_from_cond(info)
        if u_sex != cond_info_sex_age_time[0] and cond_info_sex_age_time[0] != 0:
            condition_tuple[1] = 0.1
        if u_age < cond_info_sex_age_time[1] or u_age > cond_info_sex_age_time[2]:
            condition_tuple[1] = condition_tuple[1] * 0.8
        if time < cond_info_sex_age_time[3] or time > cond_info_sex_age_time[4]:
            condition_tuple[1] = condition_tuple[1] * 1.2
        array_new.append(condition_tuple[1])
        array_normed = [i/sum(array_new) for i in array_new]
    # print("HERE_3")
    for i in range(len(new_cond_val_tuples)):
        new_cond_val_tuples[i][1] = array_normed[i]
    # print("HERE_4")
    new_cond_val_tuples = sorted(new_cond_val_tuples, key=lambda x: x[1], reverse=True)
    return new_cond_val_tuples

#evaluates user answers and returns list of top conditions and probabilities
#taking into account user information
def evaluate(symptom_init, successors, user_sub_answers, user=None):
    if user is not None:
        sex_age = extract_from_user(user)
        print("Sex_Age_Ino____________")
        print(sex_age)

    #starts with 'yes' for initial symptom
    symptom_init = get_id_from_name(symptom_init, df_related_symptoms)
    G_sympt = graph_dict[symptom_init][0]
    condition_list = graph_dict[symptom_init][2]
    network_infer = VariableElimination(G_sympt)

    symp_list_val = [1]
    symp_list_name = [symptom_init]
    for i,answer in enumerate(user_sub_answers):
        sub_sympt_id = get_id_from_name(successors[i], df_sub_symptom_names)
        symp_list_name.append(sub_sympt_id)
        if answer == True:
            print("YES: User has ", successors[i])
            symp_list_val.append(1)
        else:
            print("NO: User does not have ", successors[i])
            symp_list_val.append(0)

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
    cond_name_val_tuples = []
    for cond_val_tuple in condition_val_tuples:
        cond_id = cond_val_tuple[0]
        cond_name= get_name_from_id(cond_id, df_cond)
        cond_name_val_tuples.append([cond_name, cond_val_tuple[1]])

    print("here are probabilities")
    print(cond_name_val_tuples)
    if user is not None:
        new_cond_val_tuples = apply_personal_features(user, condition_val_tuples, 4)
        print("here are the UPDTAED using personal information probabilities")
        new_cond_name_val_tuples = []
        for new_cond_val_tuple in new_cond_val_tuples:
            new_cond_id = new_cond_val_tuple[0]
            new_cond_name= get_name_from_id(new_cond_id, df_cond)
            new_cond_name_val_tuples.append([new_cond_name, new_cond_val_tuple[1]])
        print(new_cond_name_val_tuples)
        return new_cond_name_val_tuples


    return cond_name_val_tuples

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
