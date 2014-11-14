lines = open("../data/sample_qc_input.txt", "r").readlines()
workers = {}
gold_labels = {}
qualities = {}
gold_labels['articleId1'] = "labelpos"
gold_labels['articleId2'] = "labelpos"
gold_labels['articleId3'] = "labelpos"
gold_labels['articleId4'] = "labelneg"
gold_labels['articleId5'] = "labelpos"
gold_labels['articleId6'] = "labelpos"

for line in lines:
    elems = line.strip().split()
    print elems
    if elems[1] not in workers:
        workers[elems[1]] = [0, 0]
    if elems[2] == gold_labels[elems[0]]:
        workers[elems[1]][0] += 1
    workers[elems[1]][1] += 1

for worker in workers:
    num = float(workers[worker][0])
    denom = float(workers[worker][1])
    print num/denom
    qualities[worker] = num/denom

f = open("../data/sample_qc_output.txt", "w")
for worker in qualities:
    f.write("%s %f\n" % (worker, qualities[worker]))

f.close()
    
                                                      
        
