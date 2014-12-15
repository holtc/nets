import csv 
import datetime
import matplotlib.pyplot as plt
import numpy


def smooth(close_list, beta):
    smooth = []
    smooth.append(close_list[0])
    for index in range(1, len(close_list)):
        smoothed = beta * smooth[index - 1] + (1 - beta) * close_list[index]
        smooth.append(smoothed)
    return smooth


with open('../Data/aggregated.csv','r') as f:
    reader = csv.DictReader(f, delimiter=',')
    data = list(reader)

f.close()

tweets_by_day_hour = {}

for row in data:
    day = row['date'][8:10]
    hour = row['date'][11:13]
    minute = row['date'][14:15]
    if int(hour) < 14 and int(minute) < 30:
        continue
    if int(hour) > 21:
        continue
    if int(day) < 2:
        continue
    if int(day) == 6 or int(day) == 7:
        continue
    day = ''.join(['2014-12-', day])
    if day + " " + hour not in tweets_by_day_hour.keys():
        tweets_by_day_hour[day + " " + hour] = []
    if not (row['sentiment'] == 'not_relevant'):
        tweets_by_day_hour[day + " " + hour].append((int(row['sentiment']) - 3)/2)

buckets_dict = {}

for k in tweets_by_day_hour.keys():
    buckets_dict[k] = sum(tweets_by_day_hour[k]) / float(len(tweets_by_day_hour[k]))

sorted_keys = sorted(buckets_dict)
x1 = [datetime.datetime.strptime(e, '%Y-%m-%d %H') for e in sorted_keys]
y1 = smooth([buckets_dict[i] for i in sorted_keys], .6)
plt.figure(1)
plt.plot(x1,y1, marker='o')
plt.xlim(datetime.datetime(2014, 12, 1, 0, 0),datetime.datetime(2014, 12, 11, 2, 0))
#plt.show()

with open('../Data/raw/AAPL_formatted.csv','r') as f:
    reader = csv.DictReader(f, delimiter=',')
    data = list(reader)

f.close()

close_by_day_hour = {}

for row in data:
    day = row['timestamp'][0:10]
    hour = row['timestamp'][11:13]
    if int(day[8:10]) < 2 or int(day[8:10]) > 9:
        continue
    if day + " " + hour not in close_by_day_hour.keys():
        close_by_day_hour[day + " " + hour] = []
    close_by_day_hour[day + " " + hour].append(float(row['close']))
    
buckets_dict = {}

for k in close_by_day_hour.keys():
    buckets_dict[k] = sum(close_by_day_hour[k]) / float(len(close_by_day_hour[k]))

sorted_keys = sorted(buckets_dict)
x = [datetime.datetime.strptime(e, '%Y-%m-%d %H') for e in sorted_keys]
y = smooth([buckets_dict[i] for i in sorted_keys], .6)


import numpy as np
for i in range(6):
    print np.corrcoef(y[i*8:8*(i+1)],y1[i*8:8*(i+1)])[1,0]

# plt.scatter(x,y)
# plt.show()

# indexes_to_sort_by = numpy.array(x)
# x_ordered = [] 
# y_ordered = [] 
# for i in indexes_to_sort_by:
#     x_ordered.append(x[i])
#     y_ordered.append(x[i]) 
##y_sorted = []
##
##sorted_x = sorted(x)
##for i in sorted_x:
##    y_sorted.append(y[i])
##
##y_sorted_smooth = smooth(y_sorted, 0.6)
plt.figure(2)
plt.plot(x,y, marker='o')
plt.xlim(datetime.datetime(2014, 12, 1, 0, 0),datetime.datetime(2014, 12, 11, 2, 0))

##for day in tweets_by_hour.keys():
##    for hour in tweets_by_hour[day].keys():
##        for minute in tweets_by_hour[day][hour].keys(): 
##            score = 0
##            tweet_num = 0
##            for tweet in tweets_by_hour[day][hour][minute]:
##                tweet_num += 1;
##                if tweet['sentiment'] == '5':
##                    score += 1
##                elif tweet['sentiment'] == '1':
##                    score -= 1
##            score_dict[day + " " + hour + ":" + minute + "0:00"] = score
##            average_score_dict[day + " " + hour + ":" + minute + "0:00"] = float(score)/float(tweet_num)
##
### print score_dict['Tue Dec 02 05:00:00']
##
##datetime_score_dict = {}
##
##average_datetime_score_dict = {}
##for e in score_dict:
##    datetime_score_dict[datetime.datetime.strptime(e, '%a %b %d %H:%M:%S')] = score_dict[e]
##    average_datetime_score_dict[datetime.datetime.strptime(e, '%a %b %d %H:%M:%S')] = average_score_dict[e]
##
##
##sorted_scores = sorted(datetime_score_dict)
##avg_sorted_scores = sorted(average_datetime_score_dict)
##
##
##y_sorted = []
##y_avg_sorted = []
##for i in avg_sorted_scores:
##    y_sorted.append(datetime_score_dict[i])
##    y_avg_sorted.append(average_datetime_score_dict[i])
##
##y_avg_sorted_smooth = smooth(y_avg_sorted, 0.7)
##
##average = numpy.mean(y_avg_sorted)
##stdev = numpy.std(y_avg_sorted)
##zscores = []
##for i in y_avg_sorted:
##    zscores.append((i - average)/float(stdev))
##
##
##average_smooth = numpy.mean(y_avg_sorted_smooth)
##stdev_smooth = numpy.std(y_avg_sorted_smooth)
##zscores_smooth = []
##for i in y_avg_sorted_smooth:
##    zscores_smooth.append((i - average_smooth)/float(stdev_smooth))

##plt.plot(sorted_scores, zscores_smooth, marker='o')
##plt.xlim(datetime.datetime(1900, 12, 1, 10, 0),datetime.datetime(1900, 12, 11, 2, 0))
##
plt.show()



