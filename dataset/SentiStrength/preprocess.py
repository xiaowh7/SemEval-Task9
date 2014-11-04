__author__ = 'seven'
import re
import langdetector

infile = open('twitter4242.txt', 'r')
outfile = open('full.csv', 'w')
outfile1 = open('tweets.csv', 'w')
isFirst = True
cnt = 0
for line in infile.readlines():
    if isFirst:
        isFirst = False
        continue
    sentiment = 'neutral'
    [pos, neg, tweet] = line.strip('\n').split('\t')
    score = float(pos) - float(neg)
    if score > 0:
        sentiment = 'positive'
    elif score < 0:
        sentiment = 'negative'

    # print tweet
    # chk = re.match(r'([a-zA-z0-9 \+\?\.\*\^\$\(\)\[\]\{\}\|\\/:;\'\"><,.#@!~`%&-_=])+$', tweet)
    # if not chk:
    #     tweet = ''
    if not tweet == '':
        if langdetector.detect_language(tweet) == 'english':
            cnt += 1
            tweetID = cnt
            userID = cnt
            outfile.write('%s\t%s\t%s\t%s\n' % (tweetID, userID, sentiment, tweet))
            outfile1.write('%s\n' % tweet)