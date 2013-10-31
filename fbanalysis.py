import random
import operator

def get_sentiment(current_user, users, threads):
    friend_msg_count = {}
    for thread in threads:
        for comments in thread:
            for comment in comments:
                friend_msg_count[comment.id] = friend_msg_count[comment.id] + 1
    friend_msg_count[current_user.id] = 0
    max_comments = max(friend_msgcount.iteritems(), key=operator.itemgatter(1))[0]
    def outlook(user):
        return friend_msg_count[user.id]/max_comments*20 - 10

    current_gender = current_user.gender
    current_rel_status = current_user.relationship_status
    current_sig_other = current_user.significant_other[1]
    def romance(user):
        if user.id == current_sig_other:
            return 10
        else if current_rel_status == "Single" && user.relationship_status == "Single":
            return 7
        else if current_gender != user.gender:
            return 3
        else:
            return -2

    return dict([(ui, {
        'outlook': outlook(u),
        'romance': romance(u)
        }) for ui, u in users.items()])
