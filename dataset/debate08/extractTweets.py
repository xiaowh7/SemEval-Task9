__author__ = 'seven'
outfile = open('train_example_tweets.txt', 'w')
infile = open('Apoorv_train.csv', 'r')
for line in infile.readlines():
    tweet = line.strip('\n').split('\t')[3]
    outfile.write("%s\n" % tweet)
infile.close()

infile = open('dev.csv', 'r')
for line in infile.readlines():
    tweet = line.strip('\n').split('\t')[3]
    outfile.write("%s\n" % tweet)
infile.close()
outfile.close()

outfile = open('test_example_tweets.txt', 'w')
infile = open('Apoorv_test.csv', 'r')
for line in infile.readlines():
    tweet = line.strip('\n').split('\t')[3]
    outfile.write("%s\n" % tweet)
infile.close()
outfile.close()