from textblob import TextBlob
import csv

prdtlabel = []
predictFIle = open('taskB.pred', 'r')
for line in predictFIle.readlines():
    prdtlabel.append(line.strip('\n'))

testFile = open('../dataset/test-gold-B.csv', 'r')
csvreader = csv.reader(testFile, delimiter='\t')

outfile = open('ans1.txt', 'w')
csvwriter = csv.writer(outfile, delimiter='\t')

index = -1
count = 0
cntNeu = 0
cntPos = 0
cntNeg = 0
for line in csvreader:
    index += 1
    text = TextBlob(line[3])
    if text.sentiment.subjectivity < 0.1:
        if line[2] == 'neutral':
            cntNeu += 1
        else:
            line[2] = 'neutral'
    elif text.sentiment.polarity > 0.4:
        if line[2] == 'positive':
            cntPos += 1
        else:
            line[2] = 'positive'
    elif text.sentiment.polarity < -0.2:
        if line[2] == 'negative':
            cntNeg += 1
        else:
            line[2] = 'negative'
    else:
        count += 1
        line[2] = prdtlabel[index]
    csvwriter.writerow(line)

print count, 3267-count
print cntNeu, cntPos, cntNeg