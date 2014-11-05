__author__ = 'seven'
count = 0
poscnt = 0
negcnt = 0
neucnt = 0
inFile = open('Apoorv_train.csv', 'r')

outFile = open("train_without_neutral.csv", "w")
for line in inFile.readlines():
    data = line.strip("\n").split('\t')
    count += 1
    sentiment = data[2]
    if sentiment == 'positive':
        poscnt += 1
        outFile.write(line)
    elif sentiment == 'neutral':
        neucnt += 1
    elif sentiment == 'negative':
        negcnt += 1
        outFile.write(line)

print poscnt, neucnt, negcnt, count