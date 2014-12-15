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


with open('aggregated.csv','r') as f:
    reader = csv.DictReader(f, delimiter=',')
    data = list(reader)

    

tweets_by_hour = {}

for row in data:
    day = row['date'][0:10]
    hour = row['date'][11:13]
    minute = row['date'][14:16]
    if (int(hour) < 9 or int(hour) > 16) : continue
    if (int(hour) >= 9 and int(hour) < 10 and int(minute) < 30) : continue
    if day not in tweets_by_hour.keys():
        tweets_by_hour[day] = {}
    if hour not in tweets_by_hour[day].keys():
        tweets_by_hour[day][hour] = {}
    minute = minute[0:1]
    if minute not in tweets_by_hour[day][hour].keys():
        tweets_by_hour[day][hour][minute] = []
    
    tweets_by_hour[day][hour][minute].append(row)
    
score_dict = {}
average_score_dict = {}

for day in tweets_by_hour.keys():
    for hour in tweets_by_hour[day].keys():
        for minute in tweets_by_hour[day][hour].keys(): 
            score = 0
            tweet_num = 0
            for tweet in tweets_by_hour[day][hour][minute]:
                tweet_num += 1;
                if tweet['sentiment'] == '5':
                    score += 1
                elif tweet['sentiment'] == '1':
                    score -= 1
            score_dict[day + " " + hour + ":" + minute + "0:00"] = score
            average_score_dict[day + " " + hour + ":" + minute + "0:00"] = float(score)/float(tweet_num)

# print score_dict['Tue Dec 02 05:00:00']

datetime_score_dict = {}

average_datetime_score_dict = {}
for e in score_dict:
    datetime_score_dict[datetime.datetime.strptime(e, '%a %b %d %H:%M:%S')] = score_dict[e]
    average_datetime_score_dict[datetime.datetime.strptime(e, '%a %b %d %H:%M:%S')] = average_score_dict[e]


sorted_scores = sorted(datetime_score_dict)
avg_sorted_scores = sorted(average_datetime_score_dict)


y_sorted = []
y_avg_sorted = []
for i in avg_sorted_scores:
    y_sorted.append(datetime_score_dict[i])
    y_avg_sorted.append(average_datetime_score_dict[i])

y_avg_sorted_smooth = smooth(y_avg_sorted, 0.7)

average = numpy.mean(y_avg_sorted)
stdev = numpy.std(y_avg_sorted)
zscores = []
for i in y_avg_sorted:
    zscores.append((i - average)/float(stdev))


average_smooth = numpy.mean(y_avg_sorted_smooth)
stdev_smooth = numpy.std(y_avg_sorted_smooth)
zscores_smooth = []
for i in y_avg_sorted_smooth:
    zscores_smooth.append((i - average_smooth)/float(stdev_smooth))

plt.plot(sorted_scores, zscores_smooth, marker='o')
plt.xlim(datetime.datetime(1900, 12, 1, 10, 0),datetime.datetime(1900, 12, 11, 2, 0))

plt.show()



