import os.path
import pickle
import tweet_feature_gen

def get_feature_map(tweet_data):
	feature_index = {}
	features = "feature_map.pickle"
	if os.path.isfile(features):
		f = open(features)
		feature_index = pickle.load(f)
		f.close()
	else: 
		feature_index = tweet_feature_gen.get_feature_dict_from_corpus(tweet_data)
		f = open(features, "wb")
		pickle.dump(feature_index, f)
		f.close()
	return feature_index
	