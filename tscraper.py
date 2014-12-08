""" NETS 213 Final Project
    Twitter Scraper

"""
import base64
import requests
import json
import urllib

def get_access_token():
    ''' Implement application-only authentication, as described here:
    https://dev.twitter.com/docs/auth/application-only-auth

    Note: to base64 encode a string in Python, use the b64encode
    method of the base64 class. See here:
    https://docs.python.org/2/library/base64.html

    This function should return an access token, which can then be used
    to make authenticated requests in the remainder of the homework.

    With regards to style, it's worth thinking about how many times
    you should need to call this function.
    '''
    ckey = 'U0P64ublAENwHcZ5lwgCADLHH'
    csecret = 'n19TRpI1rXhZrXtgmFvY61csTJS1g4mk2n6aL2HnTtGTfQeCVf'
    creds = base64.b64encode('{}:{}'.format(ckey, csecret))
    ct = 'application/x-www-form-urlencoded;charset=UTF-8'
    headers = {'Authorization': 'Basic {}'.format(creds), 'Content-Type': ct}
    data = 'grant_type=client_credentials'
    url = 'https://api.twitter.com/oauth2/token'
    req = requests.post(url, headers=headers, data=data)
    acc_tok = req.json()['access_token']
    return 'Bearer {}'.format(acc_tok)


atoken = get_access_token()


class TwitterSearch(object):

    ''' A Twitter search entity

    '''
    def __init__(self, search, since_id, max_id):            
        self.search = urllib.quote(search)
        self.min_id = float("inf")
        self.tweets = []
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        header = {'Authorization': atoken}
        params = {'q': self.search, 'lang': 'en'}
        if (since_id):
            params['since_id'] = since_id;
        if max_id:
            params['max_id'] = max_id
        req = requests.get(url, headers=header, params=params)
        req.raise_for_status()
        tw = req.json()
        self.max_id = tw['search_metadata']['max_id']
        for t in tw['statuses']:
            new_tweet = Tweet(t, search)
            self.tweets.append(new_tweet)
            if (new_tweet.id < self.min_id):
                self.min_id = new_tweet.id

    def __repr__(self):
        return self.search

    #appends to file
    def save_file(self, path):
        f = open(path, "a") 
        for tweet in self.tweets:
#            if isinstance(tweet.text, str):
#                print "ordinary string"
#            elif isinstance(tweet.text, unicode):
#                print "unicode string"
#            else:
#                print "not a string"
            s = '\n'.join([str(tweet.id), str(tweet.date), (tweet.text).encode('utf-8'), '\n'])
            f.write(s)
        f.close()
        
    def __str__(self):
        s = ''
        for tweet in self.tweets:
            s = ''.join([s, tweet])
        return s
            
    __repr__ = __str__
        


class Tweet(object):
    ''' An entity corresponding to a single tweet.
    '''
    def __init__(self, tdict, srch):
    	self.s = srch
    	self.id = tdict['id']
        self.text = tdict['text']
        #hashtags is not in the tweet response,
        #we will need to do this on our own
        self.date = tdict['created_at']
    
    def __str__(self):
        return ''.join([
        'Tweet Id: ', str(tweet.id), '\n',
        'Date: ', str(tweet.date), '\n',
        (tweet.text).encode('utf-8'), '\n'
        ])
        
    __repr__ = __str__


def main():
    import doctest
    options = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    print "Running doctests..."
    searches = []
    doctest.testmod(optionflags=options)
    query = "#AAPL OR @Apple"
    ts = TwitterSearch(query, None, None)
    searches.append(ts)
    filename = ''.join(['data/raw/twittersearch/', query])
    count = 0
    #make sure there are tweets returned
    while ts.tweets:
        count += 1
        if count % 500 == 0:
            print str(count) + " tweets collected"
        #save it here because we know there are tweets to save
        searches.append(ts)
        #now get next batch of tweets
        #params are query, since_id and max_d, eg the range of tweets to search
        #need to find automatic way of 
        ts = TwitterSearch(query, None, ts.min_id - 1)
    
    #goes through searches backwards, to add most recent
    #to the end, so if we run later, we can easily
    #add to the most recent to the end of the file
    #since this is much easier to do than appending
    #to the beginning of the file
    #we also should probably just put it in a db
    for search in searches[::-1]:
        search.save_file(filename)


if __name__ == "__main__":
    main()
