import json
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_oauth import OAuth

import config
import fbanalysis

app = Flask(__name__)
app.debug = getattr(config, 'DEBUG', True)
app.secret_key = getattr(config, 'SECRET_KEY', '')
oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=config.FACEBOOK_APP_ID,
    consumer_secret=config.FACEBOOK_APP_SECRET,
    request_token_params={ 'scope': 'read_mailbox' }
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('sentiment',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/logout')
def logout():
    return 'Currently not implemented'

@app.route('/sentiment')
@facebook.authorized_handler
def sentiment(res):
    if res is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (res['access_token'], '')
    me = facebook.get('/me')
    inbox = facebook.get('/me/inbox')
    threads = []
    users = {}
    for t in inbox.data['data']:
        if u'to' in t:
            for u in t[u'to'][u'data']:
                users[u['id']] = u
                # this is too slow
                # users[user_id] = facebook.get('/' + user_id + '?fields=id,name,picture').data
        if u'comments' in t:
            if u'data' in t[u'comments']:
                threads.append(t[u'comments'][u'data'])
    sentiment = fbanalysis.get_sentiment(me.data, users, threads)
    return render_template('sentiment.html', sentiment=sentiment,
        users=users.values(), me=me.data)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()