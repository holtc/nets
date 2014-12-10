from Tweet import *
from Database import *

def print_all_tweets_to_csv(db):
    f = open("../data/raw/tweets.csv", 'w')
    query = "select * from nets.tweet"
    result = db.execute(query)
    f.write("id,date,text,query\n")
    count = 0
    for r in result:
        count +=1
        text = r[2]
        s = ''.join([str(r[0]), ",", r[1], ',"', text, '",', r[3], "\n"])
        f.write(s);
    f.close()
    print "CSV contains %d tweets" % count

host = 'localhost'
user = 'nets'
pwd = 'test'
db_name = 'nets'
db = Database(host, user, pwd, db_name)
print_all_tweets_to_csv(db)
