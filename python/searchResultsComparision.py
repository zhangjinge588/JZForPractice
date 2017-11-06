import json, urllib.request

import sys

import numpy as np
import pandas as pd

import sys

def precision(tp, fp):
	return tp * 1.0 / (tp + fp)

def recall(tp, fn):
	return tp * 1.0 / (tp + fn)

try:
	searchTerm = sys.argv[1].replace(" ", "%20")

	# print (searchTerm)
except Exception as e:
	print ("First Argument Should be A Search Term")

try:
	count = sys.argv[2]
except Exception as e:
	print ("Second Argument Should be A Count in Integer")

# print (link)

# link = 'http://ha-proxy-search-prod-central.kohls.com:443/search?count=' + str(count) + '&keyword=' + searchTerm + '&explainResults=true'

# with urllib.request.urlopen(link) as url:

# 	searchResultSolr = json.loads(url.read().decode())


# productListSolr = searchResultSolr['searchResultInfo']['resultProductIdList']

# print (productListSolr)

all_distances = []

searchTerm = searchTerm.replace("%20", " ")

df = pd.read_csv('/kohls/stage/jinge/data/searchResultsPVTrim.csv', sep='~', header=None, names=['searchTerm_stem', 'searchTerm', 'pid', 'p1', 'p2', 'p3', 'gender', 'title', 'pidCount'])

# print (df.head())

df.loc[:, 'searchTerm'] = df.loc[:, 'searchTerm'].apply(lambda x: x.strip().replace("\'", "").strip().lower())

for searchTerm in df.searchTerm.unique().tolist():

	df_searchTerm = df[df.searchTerm == searchTerm]

	# print (df_searchTerm)


	productListGroundTruth = list(map(str, df_searchTerm['pid'].values.tolist()))

	searchTerm = sys.argv[1].replace(" ", "%20")

	count = len(productListGroundTruth)

	link = 'http://ha-proxy-search-prod-central.kohls.com:443/search?count=' + str(count) + '&keyword=' + searchTerm + '&explainResults=true'

	with urllib.request.urlopen(link) as url:

		searchResultSolr = json.loads(url.read().decode())


	productListSolr = searchResultSolr['searchResultInfo']['resultProductIdList']

	overlap = set(productListSolr) & set(productListGroundTruth)

	union = set(productListSolr) | set(productListGroundTruth)

	# productInSolrNotInGroundTruth = set(productListSolr) - overlap

	# productInGroundTruthNotInSolr = set(productListGroundTruth) - overlap

	# tp = len(overlap)

	# fn = len(productInSolrNotInGroundTruth)

	# fp = len(productInGroundTruthNotInSolr)

	# print (precision(tp, fp))

	# print (recall(tp, fn))

	jaccard_distance = len(overlap) / len(union) * 1.0

	all_distances.append(jaccard_distance)

print (np.average(np.asarray(all_distances)))



