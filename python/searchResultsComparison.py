
import json, urllib.request

import sys

import numpy as np
import pandas as pd

import re

def precision(tp, fp):
	return tp * 1.0 / (tp + fp)

def recall(tp, fn):
	return tp * 1.0 / (tp + fn)


all_distances = []

print ('Before Loading DataFrame')

df = pd.read_csv('/kohls/stage/jinge/data/searchResultsEvents.csv', sep='~', header=None, names=['searchTerm_stem', 'searchTerm', 'event_nm', 'pid', 'p1', 'p2', 'p3', 'gender', 'title', 'pidCount'])

print( 'Finish Loading DataFrame')

df.loc[:, 'searchTerm'] = df.loc[:, 'searchTerm'].apply(lambda x: x.strip().replace("\'", "").strip().lower())

searchTerm_matches = ['.*college.*dorm.*bedding.*', '.*american.*girl.*', '.*men.*shoe.*', '.*kitchenaid.*stand.*mixer.*', '.*shark.*nv.*70.*','.*lad.*boot.*', '.*christmas.*pajama.*', '.*family.*pajama.*', '.*nike.*gym.*vintage.*hoodie.*for.*wome.*', '.*junior.*overall.*', '.*youth.*boy.*sneaker.*', '.*snow.*boot.*', '.*nike.*windbreaker.*jackets.*', '.*beauty.*and.*beast.eyeshadow.*', '.*boy.*pajama.*set.*', '.*jennifer.*lopez.*clothing.*']

word_lst = df.searchTerm.unique().tolist()

#lst = [item for item in word_lst if any([re.match(pattern, item) != None for pattern in searchTerm_matches])]

#print (lst[0:10])


topKs = [5, 20, 50, 75, 100, 200]

non_productive_lst = ['college dorm bedding', 'american girl', 'mens shoess', 'kitchenaid stand mixer', 'shark nv70', 'ladies boots', 'christmas pajamas', 'family pajamas', 'nike gym vintage hoodie for wome', 'juniors overalls', 'youth boys sneakers', 'snow boots', 'nike windbreaker jackets', 'beauty and the beast eyeshadow', 'boys pajama sets', 'jennifer lopez clothing']

productive_lst = ['instant pot', 'apple watch series 2', 'fitbit', 'keurig coffee makers', 'air fryers', 'keurig', 'shark vacuums', 'bar stools', 'sheets', 'apple watch series 1', 'samsonite luggage', 'ninja blenders', 'patio furniture', 'mattress toppers', 'vacuums', 'apple watch']

all_lst = []
all_lst.extend(non_productive_lst)
all_lst.extend(productive_lst)

final_df = pd.DataFrame(index=range(len(all_lst) * len(topKs)), columns=['word', 'event_nm', 'productive', 'topK', 'jaccard_distance'])

index = 0

for topK in topKs:
	
	for event_nm in ['product view', 'purchase']:

		print (event_nm)

		i = 1

		for lst in [productive_lst, non_productive_lst]:

			all_distances = []

			for searchTerm in lst:

				df_searchTerm = df[((df.searchTerm == searchTerm) & (df.event_nm == event_nm))].sort_values('pidCount', ascending=False)

				productListGroundTruth = list(map(str, df_searchTerm['pid'].values.tolist()))

				searchTerm = searchTerm.replace(" ", "%20")

				count = min(len(productListGroundTruth), topK)

				link = 'http://ha-proxy-search-prod-central.kohls.com:443/search?count=' + str(count) + '&keyword=' + searchTerm + '&explainResults=true'

				with urllib.request.urlopen(link) as url:

					searchResultSolr = json.loads(url.read().decode())


				productListSolr = searchResultSolr['searchResultInfo']['resultProductIdList']

				overlap = set(productListSolr) & set(productListGroundTruth[0:count])

				union = set(productListSolr) | set(productListGroundTruth[0:count])

				if len(union) != 0:
					
					jaccard_distance = len(overlap) / len(union) * 1.0

					all_distances.append(jaccard_distance)

				else:
					jaccard_distance = 'n/a'

				final_df.loc[index, ['word', 'event_nm', 'productive', 'topK', 'jaccard_distance']] = [searchTerm.replace("%20", " "), event_nm, i, topK, jaccard_distance]
				
				index += 1

			i -= 1

final_df.to_csv('/kohls/stage/jinge/data/jd_new.csv', index=False)
