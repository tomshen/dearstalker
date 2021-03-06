"""
Twitter sentiment analysis.

This code performs sentiment analysis on Tweets.

A custom feature extractor looks for key words and emoticons.  These are fed in
to a naive Bayes classifier to assign a label of 'positive', 'negative', or
'neutral'.  Optionally, a principle components transform (PCT) is used to lessen
the influence of covariant features.

"""
import random
import nltk
#import tweet_features, tweet_pca
import tweet_feature_gen
import csv
#import json
import cPickle
import get_feature_map

def serialize_DictionaryProbDist(dist):
    dist_dict = {}
    for s in dist.samples():
        dist_dict[s] = dist.prob(s)
    return cPickle.dumps(dist_dict)

print "Creating feature map..."

#get feature dict
tweet_data = 'Sentiment-Analysis-Dataset/Sentiment Analysis Dataset.csv'
feature_index = get_feature_map.get_feature_map(tweet_data)

print 'Feature map has size ' + str(len(feature_index))
print "Analyzing..."

def get_feature_vector(tweet):
    fvec = {}
    for word in tweet.split():
        if word in feature_index:
            fvec[feature_index[word]] = 1
    return fvec

# read all tweets and labels
print "Opening twitter data..."
fp = open( tweet_data, 'rb' )
reader =  csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
tweets = []
for row in reader:
    tweets.append( [row[3], row[1]] );
print "Twitter data loaded!"
print "There are %d tweets loaded." % len(tweets)


# treat neutral and irrelevant the same
#for t in tweets:
#    if t[1] == 'irrelevant':
#        t[1] = 'neutral'


# split in to training and test sets
random.shuffle( tweets );
print "Start creating feature vectors..."
fvecs = [(get_feature_vector(t),s) for (t,s) in tweets]
print "Feature vectors created!"
v_train = fvecs[:len(fvecs)/3]
v_test  = fvecs[len(fvecs)/3:]


# dump tweets which our feature selector found nothing
#for i in range(0,len(tweets)):
#    if tweet_features.is_zero_dict( fvecs[i][0] ):
#        print tweets[i][1] + ': ' + tweets[i][0]


# apply PCA reduction
#(v_train, v_test) = \
#        tweet_pca.tweet_pca_reduce( v_train, v_test, output_dim=1.0 )


# train classifier
print "Beginning training..."
classifier = nltk.NaiveBayesClassifier.train(v_train);
print "Training complete!"
#classifier = nltk.classify.maxent.train_maxent_classifier_with_gis(v_train);

print "Getting 10000 best features..."
#best = classifier.most_informative_features(n=4000)
#print best.keys()
#inv_features = {}
#for key, value in feature_index.items():
#    inv_features[value] = key
#new_features = {}
#for (key, val) in best:
#    if key in inv_features:
#        new_features[inv_features[key]] = key
#f = csv.writer(open("feature_map.csv", "w"))
#for key, val in new_features.items():
#    f.writerow([key, val])


# classify and dump results for interpretation
#print '\nAccuracy %f\n' % nltk.classify.accuracy(classifier, v_test)
#print classifier.show_most_informative_features(200)


# build confusion matrix over test set
#test_truth   = [s for (t,s) in v_test]
#test_predict = [classifier.classify(t) for (t,s) in v_test]

#print 'Confusion Matrix'
#print nltk.ConfusionMatrix( test_truth, test_predict )

w = csv.writer(open("classifier_label_probdist.csv", "w"))
probdist = classifier._label_probdist
for key in probdist.samples():
    w.writerow([key, probdist.prob(key)])

w = csv.writer(open("classifier_feature_probdist.csv", "w"))
for key, val in classifier._feature_probdist.items():
    w.writerow([key, serialize_DictionaryProbDist(val)])

