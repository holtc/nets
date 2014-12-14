f = open("AAPL_1m.csv", "r")
lines = f.readlines()
f.close()
f = open("AAPL_formatted.csv", "w")
for line in lines:
    line = line.replace(",", ".")
    line = line.replace(";", ",")
    f.write(line)
f.close()

f = open("MSFT_1m.csv", "r")
lines = f.readlines()
f.close()
f = open("MSFT_formatted.csv", "w")
for line in lines:
    line = line.replace(",", ".")
    line = line.replace(";", ",")
    f.write(line)
f.close()

def smooth(close_list, beta):
    smooth = []
    smooth.append(close_list[0])
    for index in range(1, len(close_list)):
        smoothed = beta * smooth[index - 1] + (1 - beta) * close_list[index]
        smooth.append(smoothed)
    return smooth
    
