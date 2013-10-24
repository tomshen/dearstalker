import nltk
import string
import math
from nltk.classify import NaiveBayesClassifier
from operator import itemgetter
import random

def getGrams(message):
    message = ''.join(c for c in message if c not in string.punctuation)
    unigrams = nltk.word_tokenize(message)
    bigrams = nltk.util.bigrams(unigrams)
    trigrams = nltk.util.trigrams(unigrams)
    result = unigrams
    for b in bigrams:
        b0, b1 = b
        result += [b0 + " " + b1]
    for t in trigrams:
        t0, t1, t2 = t
        result += [t0 + " " + t1 + " " + t2]
    return result


def getCollocations(message):
    return nltk.Text(nltk.word_tokenize(message)).collocations()

def getCorpus(messages):
    #This will be replaced by a global variable eventually
    return [getCollocations(message) for message in messages]

def featureSet(ngrams):
    #Sort of a bag-of-words model - featuers are True iff the corresponding
    #word or phrase exists in the document
    return dict([(gram, True) for gram in ngrams])

def getTopN(message, N):
    #Uses tf-idf to estimate the significance of an ngram to prune features
    #We need labeled test data before this part can be implemented properly
    l = dict()
    for gram in getCollocations(message):
        tf = 1 #boolean frequency
        idf = log2(len(getCorpus([])) / sum(gram in doc for doc in corpus))
        l[gram] = tf*idf
    return sort(l, key=itemgetter(1))[:N]

#We need labeled test data before this part can be implemented properly
neg_datapoints = []
pos_datapoints = []
neg_features = [(featureSet(getTopN(data, 5000)), 'negative') for data in neg_datapoints]
pos_features = [(featureSet(getTopN(data, 5000)), 'positive') for data in pos_datapoints]
random.shuffle(neg_features)
random.shuffle(pos_features)
len_neg = len(neg_features)*0.7
len_pos = len(pos_features)*0.7

train_data = neg_features[:len_neg] + pos_features[:len_pos]
test_data = neg_features[len_neg:] + pos_features[len_pos:]

print 'training on %d datapoints' % len(train_data)
classifier = NaiveBayesClassifier.train(train_data)
print 'testing on %d datapoints' % len(test_data)
print 'accuracy:', nltk.classify.util.accuracy(classifier, test_data)
classifier.show_most_informative_features

