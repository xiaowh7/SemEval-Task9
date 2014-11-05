# __author__ = 'seven'
#
# """This src extracts the features and returns the features"""
# from featureExtractor import *
# from probablityModel import *
# import sys
# from classifier import *
# from prepare import *
# from collections import defaultdict
# from svmutil import *
# #from sklearn import naive_bayes
# #from sklearn.externals import joblib
#
# if __name__ == '__main__':
#
#     """check arguments"""
#     if len(sys.argv)!= 3:
#         print "Usage :: python mainDebate08.py ../dataset/finalTrainingInput.txt ../dataset/finalTestingInput"
#         sys.exit(0)
#
#     acronymDict, stopWords, emoticonsDict = loadDictionary()
#     print map(lambda (k, v): (frozenset(reduce( lambda x, y: x+y, [[i] if i not in acronymDict else acronymDict[i][0] for i in k.split()])), int(v)), [line.split('\t') for line in open("..//src//AFINN-111.txt")])

import csv
predfile = open('taskB.pred', 'r')
testfile = open('../dataset/test-gold-B.csv', 'r')
outfile = open('ans.txt', 'w')
# testfile = open('../dataset/sms-test-gold-B.csv', 'r')
# outfile = open('ans_sms.txt', 'w')
# testfile = open('../debate08/test_without_neutral.csv', 'r')
# outfile = open('ans_debate08.txt', 'w')
# testfile = open('../Apoorv/Apoorv_test.csv', 'r')
# outfile = open('ans_Apoorv.txt', 'w')
# testfile = open('../IT/full.csv', 'r')
# outfile = open('ans_IT.txt', 'w')
reader = csv.reader(testfile, delimiter='\t')
writer = csv.writer(outfile, delimiter='\t')

predlabel = []
for line in predfile.readlines():
    predlabel.append(line.strip('\n'))

index = 0
for row in reader:
    row[2] = predlabel[index]
    index += 1
    writer.writerow(row)
