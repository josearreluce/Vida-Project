import json
import os
from sqlalchemy import create_engine
import pandas as pd
import math

def fract_to_float(fract):
	num, den = fract.split('/')
	return float(num)/float(den)

def read_in_symptom_data(filename):
	js = open(filename)
	json_data = js.read()
	sympt_dict = json.loads(json_data)
	for symptom in sympt_dict:
		sympt_dict[symptom]['probabilities'] = fract_to_float(sympt_dict[symptom]['probabilities'])
	return sympt_dict

def get_names_from_db(engine):
	names = pd.read_sql("select name from sub_symptom_names", engine)
	name_list = list(names['name'])
	return name_list

def name_list_from_dict(sympt_dict):
	symptoms = []
	for symptom in sympt_dict:
		symptoms.append(symptom)
		for sub in sympt_dict[symptom]['sub-symptoms']:
			if "dummy" in sub:
				continue
			symptoms.append(sub)
	return symptoms

def not_in_db(db_sympt, dict_sympt):
	db_sympt = set(db_sympt)
	missing = []
	for sympt in dict_sympt:
		if sympt not in db_sympt:
			missing.append(sympt)
	return missing

def sympt_in_db(not_in_db, sympt_dict):
	not_in_db = set(not_in_db)
	symptm_in_db =[]
	for symptom in sympt_dict:
		if symptom in not_in_db:
			continue
		symptm_in_db.append(symptom)
	return symptm_in_db

def replace_with_dummy(not_in_db, sympt_dict, engine):
	sub_symptoms = pd.read_sql("select * from sub_symptom_names", engine)
	in_db = sympt_in_db(not_in_db, sympt_dict)
	for sympt in in_db:
		sub_symptoms['name'] = sub_symptoms['name'].replace(sympt, "dummy "+sympt)
	return sub_symptoms

def replace_name_with_id(sympt_df, sympt_dict):
	for symptom in sympt_dict:
		for sub_symptom in sympt_dict[symptom]['sub-symptoms']:
			sympt_id = sympt_df.loc[sympt_df['name']==sub_symptom, 'sub_sympt_id'].iloc[0]
			sympt_dict[symptom]['sub-symptoms'] = [sympt_id if x==sub_symptom else x for x in sympt_dict[symptom]['sub-symptoms']]
	return sympt_dict

def initiate_sympt_df(sympt_dict):
	sympt_df_dict = {'sympt_id':[], 'name':[]}
	id=1
	for sympt in sympt_dict:
		sympt_id = 'sympt_'+str(id)
		sympt_df_dict['sympt_id'].append(sympt_id)
		sympt_df_dict['name'].append(sympt)
		id += 1
	sympt_df = pd.DataFrame.from_dict(sympt_df_dict)
	sympt_df = sympt_df.sort_values(by=['sympt_id'])
	return sympt_df

def fill_sympt_df(sympt_dict, sympt_df):
	df = sympt_df
	for sympt in sympt_dict:
		for sub_sympt in sympt_dict[sympt]['sub-symptoms']:
			df[sub_sympt]=0
			df.at[sympt_df['name']==sympt, sub_sympt] = sympt_dict[sympt]['probabilities']
	return df

def write_to_db(tbl_name, df, engine):
	df.to_sql(tbl_name, con=engine, if_exists='replace', index=False)

# Following functions are used solely to check accuracy of data 

# def still_in_db(db_sympt, dict_sympt):
# 	dict_sympt = set(dict_sympt)
# 	missing = []
# 	for sympt in db_sympt:
# 		if sympt not in dict_sympt:
# 			missing.append(sympt)
# 	return missing

# def correct_probabilities(sympt_dict):
# 	incorrect = {}
# 	for symptom in sympt_dict:
# 		length = float(len(sympt_dict[symptom]['sub-symptoms']))
# 		prob = 1/length
# 		if math.isclose(prob, sympt_dict[symptom]['probabilities']):
# 			continue
# 		incorrect[symptom] = prob
# 	return incorrect

def create_all():
	symptom_dict = read_in_symptom_data("sub_symptoms.json")
	engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
	names_in_db = get_names_from_db(engine)
	sympt_dict_list = name_list_from_dict(symptom_dict)
	out_of_db = not_in_db(names_in_db, sympt_dict_list)
	replaced = replace_with_dummy(out_of_db, symptom_dict, engine)
	id_dict = replace_name_with_id(replaced, symptom_dict)
	sympt_df = initiate_sympt_df(id_dict)
	sympt_df = fill_sympt_df(id_dict,sympt_df)
	write_to_db('sub_symptom_names', replaced, engine)
	write_to_db('related_symptoms', sympt_df, engine)

create_all()

