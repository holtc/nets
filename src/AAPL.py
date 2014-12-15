import csv
import datetime
import matplotlib.pyplot as plt


def smooth(close_list, beta):
    smooth = []
    smooth.append(close_list[0])
    for index in range(1, len(close_list)):
        smoothed = beta * smooth[index - 1] + (1 - beta) * close_list[index]
        smooth.append(smoothed)
    return smooth

with open('../Data/raw/AAPL_formatted.csv','r') as f:
    reader = csv.DictReader(f, delimiter=',')
    data = list(reader)

f.close()

close_by_day_hour = {}

for row in data:
    day = row['timestamp'][0:10]
    hour = row['timestamp'][11:13]
    if day + " " + hour not in close_by_day_hour.keys():
        close_by_day_hour[day + " " + hour] = []
    close_by_day_hour[day + " " + hour].append(float(row['close']))
    
buckets_dict = {}

for k in close_by_day_hour.keys():
    buckets_dict[k] = sum(close_by_day_hour[k]) / float(len(close_by_day_hour[k]))

sorted_keys = sorted(buckets_dict)
x = [datetime.datetime.strptime(e, '%Y-%m-%d %H') for e in sorted_keys]
y = smooth([buckets_dict[i] for i in sorted_keys], .6)

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

plt.plot(x,y, marker='o')
plt.xlim(datetime.datetime(2014, 12, 1, 0, 0),datetime.datetime(2014, 12, 11, 2, 0))
plt.show()



