import csv
import cPickle
import nltk
import random

def find_users_in_thread(thread):
    users = []
    for comment in thread:
        id = 0
        try:
            id = comment['from']['id']
        except: continue
        users.append(id)
    users_set = set(users)
    return users_set

def calc_outlook(current_user, users, threads):
    label_probdist_dict = {}
    f = csv.reader(open("classifier_label_probdist.csv", "r"))
    for key, val in f:
        label_probdist_dict[float(key)] = float(val)

    feature_probdist = {}
    f = csv.reader(open("classifier_feature_probdist.csv", "r"))
    for key, val in f:
        k = tuple([int(k) for k in eval(key)])
        feature_probdist[k] = cPickle.loads(val)
        if 1 in feature_probdist[k]:
            feature_probdist[k][0] = float(feature_probdist[k][None])
            feature_probdist[k][1] = float(feature_probdist[k][1])
        elif 0 in feature_probdist[k]:
            feature_probdist[k][1] = float(feature_probdist[k][None])
            feature_probdist[k][0] = float(feature_probdist[k][0])
        feature_probdist[k].pop(None)
        feature_probdist[k] = nltk.DictionaryProbDist(feature_probdist[k])
    label_probdist = \
        nltk.probability.DictionaryProbDist(prob_dict=label_probdist_dict)
    classifier = nltk.classify.NaiveBayesClassifier(label_probdist, feature_probdist)
    f = csv.reader(open("feature_map.csv", "r"))
    featuremap = {}
    for key, val in f:
        featuremap[key] = val

    def get_feature_vector(comment):
        fvec = {}
        words = []
        try:
            words = comment
        except:
            print 'oops'
            for feature in featuremap:
                if random.randint(1,5) == 1:
                    fvec[featuremap[feature]] = 1
            return fvec
        for word in words.split():
            if word in featuremap:
                print 'WORD', word
                fvec[int(featuremap[word])] = 1
        return fvec

    friend_outlook = {}
    for user in users.keys():
        friend_outlook[user] = 0.0
    for thread in threads:
        thread_users = find_users_in_thread(thread)
        user_comments = {}
        for user in thread_users:
            user_comments[user] = []
        for comment in thread:
            try:
                user_comments[comment['from']['id']].append(comment['message'])
            except: continue
        for user in thread_users:
            if user == current_user['id']:
                continue
            try:
                comments = user_comments[user]
            except: comments = []
            try:
                comments += user_comments[current_user['id']]
            except: comments = comments
            fvecs = [get_feature_vector(c) for c in comments]
            labels = [classifier.prob_classify(v).prob(1) for v in fvecs if len(v) != 0]
            if len(labels) == 0:
                friend_outlook[user] = 0.5
            else:
                friend_outlook[user] = sum(labels)/len(labels)

            print(user, str(fvecs))
    return friend_outlook
