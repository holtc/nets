""" NETS 213 Final Project
    Twitter Scraper

"""
import base64
import requests
import json


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

    >>> apple = TwitterSearch('#aapl')
    '''
    def __init__(self, search):
        self.search = search
        self.tweets = []
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        header = {'Authorization': atoken}
        params = {'q': search, 'lang': 'en'}
        req = requests.get(url, headers=header, params=params)
        req.raise_for_status()
        tw = req.json()
        for t in tw['statuses']:
            self.tweets.append(Tweet(t, search))

    def __repr__(self):
            return self.search


class Tweet(object):
    ''' An entity corresponding to a single tweet.
    '''
    def __init__(self, tdict, srch):
    	self.s = 
    	self.id = tdict['id']
        self.text = tdict['text']
        self.hashtags = []
        if 'hashtags' in tdict:
            self.hashtags = tdict['hashtags']
        self.date = tdict['created_at']

def main():
    import doctest
    options = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    print "Running doctests..."
    doctest.testmod(optionflags=options)


if __name__ == "__main__":
    main()
