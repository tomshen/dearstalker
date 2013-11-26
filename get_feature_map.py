import os.path
import csv
import tweet_feature_gen

def get_feature_map(tweet_data):
	feature_index = {}
	features = "feature_map.csv"
	if os.path.isfile(features):
		f = csv.reader(open(features, "r"))
                for key, val in f:
                        dict[key] = val
		f.close()
	else: 
		feature_index = tweet_feature_gen.get_feature_dict_from_corpus(tweet_data)
		f = csv.writer(open(features, "w"))
		for key, val in feature_index.items():
                        w.writerow([key, val])
		f.close()
	return feature_index
	
