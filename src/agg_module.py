q_lines = open("../data/sample_qc_output.txt", "r").readlines()
qualities = {}
for line in q_lines:
    elems = line.strip().split()
    qualities[elems[0]] = elems[1]

lines = open("../data/sample_agg_input.txt", "r").readlines()
worker_votes = {}
labels = {}
for line in lines:
    elems = line.strip().split()
    worker_id = elems[1]
    tweet_id = elems[0]
    label = elems[2]
    if tweet_id not in worker_votes:
        #first index is num pos labels, second is num neg labels
        worker_votes[tweet_id] = [0, 0]
    print worker_votes
    if label == "labelpos":
        worker_votes[tweet_id][0] += float(qualities[worker_id])
    else:
        worker_votes[tweet_id][1] += float(qualities[worker_id])
    print worker_votes

for tweet_id in worker_votes:
    if worker_votes[tweet_id][0] > worker_votes[tweet_id][1]:
        labels[tweet_id] = "labelpos"
    else:
        labels[tweet_id] = "labelneg"

f = open("../data/sample_agg_output.txt", "w")
for tweet_id in labels:
    f.write("%s %s\n" % (tweet_id, labels[tweet_id]))

f.close()
    
        
