class Tweet(object):
    ''' An entity corresponding to a single tweet.
    '''
    def __init__(self, tdict, search):
        self.search = search
        self.id = tdict['id']
        self.text = tdict['text'].replace("\\", "\\\\")
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

    #will return id if successful insert, None otherwise
    def save(self, db):
        try:
            query = "".join(['call save_tweet(', str(self.id), ', "', self.date, '", "', self.text.replace('"', "'"), '", "', self.search, '")'])
            result = db.execute(query)
            if result:
                result = result[0][0]
            return result
        except UnicodeEncodeError:
            return None
