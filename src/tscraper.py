""" NETS 213 Final Project
    Twitter Scraper

"""
import base64
import json

from Database import *
from Tweet import *
from TwitterSearch import *

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
    #ckey = 'U0P64ublAENwHcZ5lwgCADLHH'
    ckey = '8RqNDHm7vjUvdqEa3l7P6DQww'
    #csecret = 'n19TRpI1rXhZrXtgmFvY61csTJS1g4mk2n6aL2HnTtGTfQeCVf'
    csecret = 'fHlAKr8bZvIjOV0KDXN2EDI1s4DouLuIpL7sB7NpXIsfC4zfR5'
    creds = base64.b64encode('{}:{}'.format(ckey, csecret))
    ct = 'application/x-www-form-urlencoded;charset=UTF-8'
    headers = {'Authorization': 'Basic {}'.format(creds), 'Content-Type': ct}
    data = 'grant_type=client_credentials'
    url = 'https://api.twitter.com/oauth2/token'
    req = requests.post(url, headers=headers, data=data)
    acc_tok = req.json()['access_token']
    return 'Bearer {}'.format(acc_tok)
        
def get_since_id(db, search_query):
        max_id = 0
        query = 'call get_max_ids()'
        result = db.execute(query)
        for r in result:
            if r[1] == search_query:
                return long(r[0])
        return max_id

def search_twitter(atoken, query, db):
    count = 1
    since_id = get_since_id(db, query)
    max_date = '2014-12-11'
    ts = TwitterSearch(atoken, query, since_id + 1, None, max_date)
    #make sure there are tweets returned
    num_tweets = 0
    while len(ts.tweets) > 0 and count < 450:
        count += 1
        if (count % 25 == 0):
            print str(count) + " requests for: " + query + "....."
        #save it here because we know there are tweets to save
        #now get next batch of tweets
        #params are query, since_id and max_id, eg the range of tweets to search
        ts = TwitterSearch(atoken, query, since_id + 1, ts.min_id - 1, max_date)
        num_tweets += ts.save_results(db)
    print str(count) + " total requests for: " + query 
    print str(num_tweets) + " tweets saved for: " + query + '\n'
    return count

def main():
    import doctest
    atoken = get_access_token()
    host = 'localhost'
    user = 'nets'
    pwd = 'test'
    db_name = 'nets'
    db = Database(host, user, pwd, db_name)
    options = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    doctest.testmod(optionflags=options)
    queries = ["#MSFT OR @Microsoft", "#AAPL OR @Apple", "#GOOG OR @Google", "#SNE OR @Sony"]
    total_requests = 0
    for query in queries:
        total_requests += search_twitter(atoken, query, db)
    print str(total_requests) + " requests made to Twitter API"

if __name__ == "__main__":
    main()
