import random
import operator

def get_sentiment(current_user, users, threads):
    friend_msg_count = {}
    for user in users.keys():
        friend_msg_count[user] = 0
    for thread in threads:
        for comment in thread:
            try:
                sender = comment['from']['id']
                if sender not in friend_msg_count:
                    friend_msg_count[sender] = 0
            except: continue
            friend_msg_count[sender] += 1
    friend_msg_count[current_user['id']] = None
    max_comments = float(max(friend_msg_count.values()))
    def volume(user):
        if user['id'] not in friend_msg_count:
            print '%s not found in message count' % users[user['id']]['name']
        else:
            return friend_msg_count[user['id']]/max_comments * 20.0 - 10.0

    def outlook(user):
        return random.randint(-10,10)
    return dict([(ui, {
        'volume': volume(u),
        'outlook': outlook(u)
        }) for ui, u in users.items()])
