import urllib
import requests
from Tweet import *

class TwitterSearch(object):

    ''' A Twitter search entity

    '''
    def __init__(self, atoken, search, since_id, max_id, until):            
        self.search = urllib.quote(search)
        self.min_id = float("inf")
        self.tweets = []
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        header = {'Authorization': atoken}
        params = {'q': self.search, 'lang': 'en'}
        if since_id:
            params['since_id'] = since_id;
        if max_id:
            params['max_id'] = max_id
        if until:
            params['until'] = until
        req = requests.get(url, headers=header, params=params)
        if req.status_code == 200:
            tw = req.json()
            self.max_id = tw['search_metadata']['max_id']
            for t in tw['statuses']:
                new_tweet = Tweet(t, search)
                self.tweets.append(new_tweet)
                if (new_tweet.id < self.min_id):
                    self.min_id = new_tweet.id
        elif req.status_code == 429:
            print "TwitterError: Too many requests in this 15-minute window"
        else:
            print "TwitterError: " + str(req.status_code)

    def __repr__(self):
        return self.search

    #appends to file
    def save_results(self, db):
        num_tweets_saved = 0
        for tweet in self.tweets:
#            if isinstance(tweet.text, str):
#                print "ordinary string"
#            elif isinstance(tweet.text, unicode):
#                print "unicode string"
#            else:
#                print "not a string"
            last_id = tweet.save(db)
            if last_id:
                num_tweets_saved += 1
        return num_tweets_saved
        
    def __str__(self):
        s = ''
        for tweet in self.tweets:
            s = ''.join([s, tweet])
        return s
            
    __repr__ = __str__
