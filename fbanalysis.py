import random
import operator
import calc_outlook

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
        friend_outlook = calc_outlook.calc_outlook(get_sentiment, users, threads)
        for user in friend_outlook.keys():
            friend_outlook[user] = friend_outlook[user] * 20.0 - 10.0
        return friend_outlook
    

    return dict([(ui, {
        'volume': volume(u),
        'outlook': outlook(u)
        }) for ui, u in users.items()])
