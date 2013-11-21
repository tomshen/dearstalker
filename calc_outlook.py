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
    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    f = open('featuremap.pickle', 'rb')
    featuremap = pickle.load(f)
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
            if user = current_user:
                continue
            comments = user_comments[user].extend(user_comments[current_user])
            fvecs = [get_feature_vector(c) for c in comments]
            friend_outlook[user] = avg([classifier.classify(v) for v in fvecs])
    return friend_outlook
