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

with open('AAPL_formatted.csv','r') as f:
    reader = csv.DictReader(f, delimiter=',')
    data = list(reader)
    
position_by_hour = {}

for row in data:
    day = row['timestamp'][0:10]
    hour = row['timestamp'][11:13]
    minute = row['timestamp'][14:15]
    if day not in position_by_hour.keys():
        position_by_hour[day] = {}
    if hour not in position_by_hour[day].keys():
        position_by_hour[day][hour] = {}
    if minute not in position_by_hour[day][hour].keys():
        position_by_hour[day][hour][minute] = []
    position_by_hour[day][hour][minute].append(row)
# print position_by_hour['2014-12-01']['14']

avg_pos_dict = {}

for day in position_by_hour.keys():
    for hour in position_by_hour[day].keys():
        for minute in position_by_hour[day][hour].keys():
            position = 0
            count = 0
            for pos in position_by_hour[day][hour][minute]:
                count += 1;
                position += float(pos['open'])
            avg_pos_dict[day + " " + hour + ":" + minute + "0:00"] = position/float(count)

datetime_pos_dict = {}
for e in avg_pos_dict:
    dt = datetime.datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
    dt = dt.replace(hour=dt.hour - 5)
    datetime_pos_dict[dt] = avg_pos_dict[e]

x = datetime_pos_dict.keys()
print x[0].hour
y = datetime_pos_dict.values()

# plt.scatter(x,y)
# plt.show()

# indexes_to_sort_by = numpy.array(x)
# x_ordered = [] 
# y_ordered = [] 
# for i in indexes_to_sort_by:
#     x_ordered.append(x[i])
#     y_ordered.append(x[i]) 
y_sorted = []

sorted_pos_dict = sorted(datetime_pos_dict)
for i in sorted_pos_dict:
    y_sorted.append(datetime_pos_dict[i])

y_sorted_smooth = smooth(y_sorted, 0.6)

plt.plot(sorted_pos_dict,y_sorted_smooth, marker='o')
plt.xlim(datetime.datetime(2014, 12, 1, 0, 0),datetime.datetime(2014, 12, 11, 2, 0))
plt.show()



