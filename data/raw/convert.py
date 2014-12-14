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
    
