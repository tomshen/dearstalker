import nltk

def find_users_in_thread(thread):
    users = []
    for comment in thread:
        try:
            users.add(comment['from']['id'])
        except: continue
    users_set = set(users)
    return users_set

def get_feature_vector(comment):
    fvec = {}
    for i in feature_index:
        fvec[i] = 0
    try:
        for word in comment['content'].split():
            if word in feature_index:
                fvec[feature_index[word]] = 1
        return fvec
    except: return fvec

def calc_outlook(current_user, users, threads):
    label_probdist_dict = {}
    f = csv.reader(open("classifier_label_probdist.csv", "r"))
    for key, val in f:
        label_probdist_dict[key] = val
    f.close()

    feature_probdist = {}
    f = csv.reader(open("classifier_feature_probdist.csv", "r"))
    for key, val in f:
        feature_probdist[key] = val
    f.close()

    label_probdist = \
        nltk.probability.DictionaryProbDist(prob_dict=label_probdist_dict, normalize=True)
    classifier = nltk.classify.NaiveBayesClassifier(label_probdist, feature_probdist)

    f = csv.reader(open("featuremap.csv", "r"))
    featuremap = {}
    for key, val in f:
        featuremap[key] = val
    f.close()

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
                user_comment[comment['from']['id']].add(comment['text'])
            except: continue
        for user in thread_users:
            if user == current_user:
                continue
            comments = user_comments[user].extend(user_comments[current_user])
            fvecs = [get_feature_vector(c) for c in comments]
            friend_outlook[user] = avg([classifier.classify(v) for v in fvecs])
    return friend_outlook
