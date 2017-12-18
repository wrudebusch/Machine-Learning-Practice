from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup as soup
import time
import datetime
import random
import pandas as pd
import csv

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def pull_4chan():
	## opening connection, grabbing page
	website_req = Request('http://boards.4chan.org/b/catalog', headers={'User-Agent': 'Mozilla/5.0'})
	raw_webpage = urlopen(website_req).read().decode('utf-8','ignore')
	## parsing raw html data
	script_text = soup(raw_webpage, "html.parser").findAll('script')
	for s in script_text:
		if "catalog =" in str(s):
			threads_body = str(s).split("catalog = ")
			return pd.read_json(threads_body[1].split(";var")[0])
			break

	#data = pd.read_json(threads_body[6][9:-1])
	#return data['threads']

#print(y.columns)
# while True:
# 	x = pd.read_json(pull_4chan())
#	ts = time.time()
# 	st = datetime.datetime.fromtimestamp().strftime('%Y-%m-%d %H:%M:%S')
# 	x['threads'].to_csv("chan_dump"+str(st)+".csv", index='false')
# 	time.sleep(60*random.randint(10, 60))

threads = pull_4chan()
#print(threads['threads'])

file_name = "r9k_dump_"+str(ts)+".csv"
threads['threads'].to_csv(file_name,index=False)

# with open(file_name, 'w') as csvfile:
#     fieldnames = ['_date', 'post', 'teaser']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for i, j in enumerate(threads):
#     	print(i,j,threads[i]['teaser'])
#     	writer.writerow({'_date': st, 'post': i, 'teaser': threads[i]['teaser']})