__author__ = 'seven'
from textblob import TextBlob
import csv
# testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
# print testimonial.sentiment
# print testimonial.sentiment.polarity
index = -1
cntPos = 0
cntNeg = 0
cntNeu = 0

countofSubjectivity = 0
countofPositive = 0
countofNegative = 0

errorPos = 0
errorNeg = 0
errorNeu = 0

correctPos = 0
correctNeg = 0
correctNeu = 0

prdtlabel = []
predictFIle = open('taskB.pred', 'r')
for line in predictFIle.readlines():
    prdtlabel.append(line.strip('\n'))


infile = open('../dataset/test-gold-B.csv', 'r')
reader = csv.reader(infile, delimiter='\t')
for line in reader:
    index += 1
    sentiment = line[2]
    text = TextBlob(line[3])
    if sentiment == 'positive':
        cntPos += 1
        if text.sentiment.polarity > 0.4:
            countofPositive += 1
            if not prdtlabel[index] == 'positive':
                errorPos += 1
                print "positive -> %s" % prdtlabel[index]

    if sentiment == 'negative':
        cntNeg += 1
        if text.sentiment.polarity < -0.2:
            countofNegative += 1
            if not prdtlabel[index] == 'negative':
                errorNeg += 1
                print "negative -> %s" % prdtlabel[index]

    if sentiment == 'neutral':
        cntNeu += 1
        if text.sentiment.subjectivity < 0.3:
            countofSubjectivity += 1
            if not prdtlabel[index] == 'neutral':
                errorNeu += 1
                print "neutral -> %s, polarity=%s" % (prdtlabel[index], text.sentiment.polarity)

print cntPos, countofPositive, errorPos
print cntNeg, countofNegative, errorNeg
print cntNeu, countofSubjectivity, errorNeu


