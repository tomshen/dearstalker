import random
import operator

def get_sentiment(current_user, users, threads):
    friend_msg_count = {}
    for user in users.keys():
        friend_msg_count[user] = 0
    for thread in threads:
        for comment in thread:
            sender = comment['from']['id']
            if sender not in friend_msg_count:
                friend_msg_count[sender] = 0
            friend_msg_count[sender] += 1
    friend_msg_count[current_user['id']] = None
    max_comments = float(max(friend_msg_count.values()))
    def outlook(user):
        if user['id'] not in friend_msg_count:
            print '%s not found in message count' % users[user['id']]['name']
        else:
            return friend_msg_count[user['id']]/max_comments * 20.0 - 10.0

    """
    current_gender = current_user['gender']
    current_rel_status = current_user['relationship_status']
    current_sig_other = current_user['significant_other']['id']
    def romance(user):
        if user['id'] == current_sig_other:
            return 10
        elif current_rel_status == "Single" and user['relationship_status'] == 'Single':
            return 7
        elif current_gender != user['gender']:
            return 3
        else:
            return -2
    """
    def romance(user):
        return random.randint(-10,10)
    return dict([(ui, {
        'outlook': outlook(u),
        'romance': romance(u)
        }) for ui, u in users.items()])
