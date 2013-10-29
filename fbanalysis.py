import random

def get_sentiment(current_user, users, threads):
    return dict([(ui, {
        'outlook': random.randint(-10,10),
        'romance': random.randint(-10,10)
        }) for ui, u in users.items()])