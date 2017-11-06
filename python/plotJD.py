import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def convert(x):
	if x == 'n/a':
		return np.float(0)
	else:
		return np.float(x)

def getProductive(x):
	if x == 1:
		return 'productive'
	else:
		return 'non-productive'

df = pd.read_csv('/Users/tkmaeiz/Desktop/jd_new.csv')

df.jaccard_distance = df.jaccard_distance.apply(lambda x: convert(x))

event_nms = df.event_nm.unique().tolist()

productives = df.productive.unique().tolist()

topKs = df.topK.unique().tolist()

f, axs = plt.subplots(len(event_nms), len(productives), sharex='col', sharey='row')

colors = ['red', 'gold', 'blue', 'green', 'pink', 'purple']

for i in range(len(event_nms)):

	for j in range(len(productives)):

		ax = axs[i][j]

		ax.set_title(event_nms[i] + "_" + getProductive(productives[j]))

		temp_df = df[((df.event_nm == event_nms[i]) & (df.productive == productives[j]))]

		for k in range(len(topKs)):

			x = temp_df[temp_df.topK == topKs[k]].word.values.tolist()
			y = temp_df[temp_df.topK == topKs[k]].jaccard_distance.values.tolist()

			ax.set_xticks(range(len(x)))
			ax.set_xticklabels(x, rotation=90)

			# print (event_nms[i], productives[j], len(x))

			ax.plot(range(len(x)), y, '-', color=colors[k], label=str(topKs[k]))

		ax.legend(loc='best')

plt.show()


		





