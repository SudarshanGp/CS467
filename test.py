import json
import csv
import pprint
f = open('text1.json')
data = json.load(f)
f.close()
f=csv.writer(open('test.csv','wb+'))

