import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os

def conditions_df(xlwkbk):
	return pd.read_excel(xlwkbk)

def get_and_order_symptoms(df):
	main_df = df
	symptom_list_main = main_df['symptoms']
	symptom_str = ','.join(symptom_list_main)
	symptom_list = symptom_str.split(',')
	symptom_set = set(symptom_list)
	symptom_list = list(symptom_set)
	
	sympt_id = {}
	id_key = 1
	for symptom in symptom_list:
		sympt_id[symptom] = "sympt_"+str(id_key)
		id_key += 1

	numeric_symptoms = []
	for cond in symptom_list_main:
		sympt_ids = []
		symptom_list = cond.split(',')
		for symptom in symptom_list:
			sympt_ids.append(sympt_id[symptom])
		numeric_symptoms.append(sympt_ids)
	main_df['symptom_ids'] = numeric_symptoms
	return sympt_id, main_df

def create_binary_cond_df(sympt_dict, cond_df):
	main_cond_df = cond_df
	for symptom in sympt_dict:
		col_name = sympt_dict[symptom]
		main_cond_df[col_name] = 0

	cond_symptoms = main_cond_df['symptom_ids']
	for i in range(len(cond_symptoms)):
		for symptom in cond_symptoms[i]:
			main_cond_df.at[i, symptom] = 1
	main_cond_df=main_cond_df.drop(labels=['symptoms', 'symptom_ids'], axis=1)
	return main_cond_df

def create_binary_sympt_df(sympt_dict, cond_df):
	sympt_df_dict = {'sympt_id':[], 'name':[]}
	for symptom in sympt_dict:
		sympt_df_dict['sympt_id'].append(sympt_dict[symptom])
		sympt_df_dict['name'].append(symptom)
	sympt_df = pd.DataFrame.from_dict(sympt_df_dict)
	sympt_df = sympt_df.sort_values(by=['sympt_id'])
	
	cond_id = cond_df['cond_id']
	i = 0
	for id in cond_id:
		sympt_df[id] = 0
		for sympt_id in sympt_df['sympt_id']:
			if cond_df.loc[cond_df['cond_id']==id, sympt_id].item() == 1:
				sympt_df.at[sympt_df['sympt_id']==sympt_id, id] = 1
	return sympt_df




def write_to_db(tbl_name, df):
	engine = create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
	df.to_sql(tbl_name, con=engine, if_exists='replace', index=False)

def main():
	conditions = conditions_df('Conditions_and_symptoms.xlsx')
	sympt_id, conditions = get_and_order_symptoms(conditions)
	conditions = create_binary_cond_df(sympt_id, conditions)
	symptoms = create_binary_sympt_df(sympt_id, conditions)

	write_to_db('conditions', conditions)
	write_to_db('symptoms', symptoms)

main()
