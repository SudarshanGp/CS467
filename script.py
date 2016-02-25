import json
from pprint import pprint
from itertools import * 
import csv as csv
import pandas as pd

data = {}
with open('data.json') as data_file:    
    data = json.load(data_file)

entries = data['payload']['entries']
new_data = {}
new_data_users = []
new_data_groups = []
new_data_pages = []
new_data_apps = []

for i, val in enumerate(entries):
	if(val['type'] == 'user'):
		val['name'] = val['text'].encode("utf8")
		val['Score'] = val['grammar_costs']['{user}'] 
		new_data_users.append(val);
	elif(val['type'] == 'group'):
		val['name'] = val['text'].encode("utf8")
		val['Score'] = val['grammar_costs']['{group}'] 
		new_data_groups.append(val)
	elif(val['type'] == 'page'):
		val['name'] = val['text'].encode("utf8")
		try:
			val['Score'] = val['grammar_costs']['{page}']			
			new_data_pages.append(val)
		except KeyError:
			pass
	elif(val['type'] == 'app'):
		val['name'] = val['text'].encode("utf8")
		val['Score'] = val['grammar_costs']['{app}']
		new_data_apps.append(val)
	else:
		continue

new_data_users = pd.DataFrame(new_data_users)
new_data_users_modified = new_data_users[['name', 'Score', 'type']]
new_data_users_modified = new_data_users_modified.ix[1:]
new_data_groups = pd.DataFrame(new_data_groups)
new_data_groups_modified = new_data_groups[['name', 'Score', 'type']]
new_data_pages = pd.DataFrame(new_data_pages)
new_data_pages_modified = new_data_pages[['name', 'Score', 'type']]
new_data_apps = pd.DataFrame(new_data_apps)
new_data_apps_modified = new_data_apps[['name', 'Score', 'type']]
temp = [new_data_users_modified, new_data_groups_modified, new_data_pages_modified, new_data_apps_modified]
new_df = pd.concat(temp, ignore_index = True)
# new_df['Score'] = new_df['Score'] *1
new_df = new_df.sort('Score')
#new_df = new_df[::-1]
new_df = new_df.reset_index(drop = True)
number_of_entries = len(new_df['name'])
top_10 = ['0-10%'] * (number_of_entries/10)
top_20 = ['10-20%'] * (number_of_entries/10)
top_30 = ['20-30%'] * (number_of_entries/10)
top_40 = ['30-40%'] * (number_of_entries/10)
top_50 = ['40-50%'] * (number_of_entries/10)
top_60 = ['50-60%'] * (number_of_entries/10)
top_70 = ['60-70%'] * (number_of_entries/10)
top_80 = ['70-80%'] * (number_of_entries/10)
top_90 = ['80-90%'] * (number_of_entries/10)
top_100 = ['90-100%'] * (number_of_entries- 9*(number_of_entries/10))
new_list = top_10 + top_20 + top_30 + top_40 + top_50 + top_60 + top_70 + top_80 + top_90 + top_100
new_df['rank'] = new_list
new_df['index'] = 1
new_df.to_csv('facebook.csv')

