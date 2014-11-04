# __author__ = 'seven'
# from featureExtractor import *
# from prepare import *
#
# def findEmoticons(tweet, token):
#     countEmoPos = 0
#     countEmoNeg = 0
#     # countEmoExtremePos = 0
#     # countEmoExtremeENeg = 0
#     isLastEmoPos = 0
#     isLastEmoNeg = 0
#     isLastTokenEmoPos = 0
#     isLastTokenEmoNeg = 0
#
#     for i in range(len(tweet)):
#         if token[i] == 'E':
#             if tweet[i] == 'Extremely-Positive' or tweet[i] == 'Positive':
#                 # countEmoExtremePos += 1
#                 countEmoPos += 1
#                 isLastEmoPos = 1
#                 isLastEmoNeg = 0
#             if tweet[i] == 'Extremely-Negative' or tweet[i] == 'Negative':
#                 # countEmoExtremeENeg += 1
#                 countEmoNeg += 1
#                 isLastEmoPos = 0
#                 isLastEmoNeg = 1
#
#             if i == len(tweet) - 1:
#                 # print "The last token is Emoticon %s" % tweet[i]
#                 if tweet[i] == 'Extremely-Positive' or tweet[i] == 'Positive':
#                     isLastTokenEmoPos = 1
#                 if tweet[i] == 'Extremely-Negative' or tweet[i] == 'Negative':
#                     isLastTokenEmoNeg = 1
#     return [countEmoPos, countEmoNeg, isLastEmoPos, isLastEmoNeg, isLastTokenEmoPos, isLastTokenEmoNeg]
#
# if __name__ == "__main__":
#     """create emoticons dictionary"""
#     f = open("emoticonsWithPolarity.txt", 'r')
#     data = f.read().split('\n')
#     emoticonsDict = {}
#     for i in data:
#         if i:
#             i = i.split()
#             value = i[-1]
#             key = i[:-1]
#             for j in key:
#                 emoticonsDict[j] = value
#     f.close()
#
#     #print emoticonsDict
#
#     index = 0
#     poscrc = 0
#     negcrc = 0
#     poscount = 0
#     negcount = 0
#     pospre = 0
#     negpre = 0
#     count = 0
#     f = open('../dataset/final_test-gold-B_Input.txt', 'r')
#     for line in f:
#         if line:
#             index += 1
#             # print line
#             line = line.strip('\n').split('\t')
#             tweet = line[1].split()
#             token = line[2].split()
#             label = line[3].strip()
#             # if tweet and not label == 'neutral':
#             if tweet:
#                 posscore = 0
#                 negscore = 0
#                 count += 1
#                 # tweet, token, count1, count2 = preprocesingTweet1(tweet, token, emoticonsDict, acronymDict)
#                 # tweet = [i.strip(specialChar).lower() for i in tweet]
#                 tweet, token = replaceEmoticons(emoticonsDict, tweet, token)
#                 tweet, countNegation = replaceNegation(tweet)
#                 tweet = [i for i in tweet if i]
#                 [countEmoPos, countEmoNeg, isLastEmoPos, isLastEmoNeg, isLastTokenEmoPos, isLastTokenEmoNeg] = findEmoticons( tweet, token)
#                 # print countEmoPos, countEmoNeg, isLastEmoPos, isLastEmoNeg, isLastTokenEmoPos, isLastTokenEmoNeg
#                 # if countEmoPos + countEmoNeg > 0:
#                 #     count += 1
#                 posscore = countEmoPos
#                 negscore -= countEmoNeg
#                 total = posscore+negscore
#                 if not total == 0:
#                     print "Index: %d, Positive Score: %f, Negtive Score: %f, Total Score: %f, Label: %s" % (
#                         index, posscore, negscore, total, label)
#
#                 if label == 'positive':
#                     poscount += 1
#                 elif label == 'negative':
#                     negcount += 1
#
#                 if total > 0 and not countNegation:
#                     pospre += 1
#                     if label == 'positive':
#                         poscrc += 1
#                 elif total < 0:
#                     negpre += 1
#                     if label == 'negative':
#                         negcrc += 1
#
#     print poscrc, pospre, poscount
#     print "Positive, Precision: %f, Recall: %f, " % ( float(poscrc)/pospre, float(poscrc)/poscount )
#     print negcrc, negpre, negcount
#     print "Negative, Precision: %f, Recall: %f, " % ( float(negcrc)/negpre, float(negcrc)/negcount )
#     f.close()
#     # print count

# from svmutil import *
# model = svm_load_model('sentimentAnalysisSVM.model')
import re
from getDependency import getDependency
# ans = getDependency()
# for dpd in ans:
#     print dpd
# ans = [[2, 3], [4, 5]]
# for list in ans:
#     print list[0]
from prepare import *
from featureExtractor import *
# acronymDict, stopWords, emoticonsDict = loadDictionary()
# print emoticonsDict
# exit(0)
# S140Unigram, S140Bigram, S140Pairgram = loadS140Lexicon()
# NRCUnigram, NRCBigram, NRCPairgram = loanNRCLexicon()
#
# count = 0
# for word in S140Unigram:
#     if word == "no" or word == "not" or word.count("n't") > 0:
#         count += 1
#         print count, word, S140Unigram[word]
#
# for word in S140Bigram:
#     if word.count("no") > 0 or word.count("not") > 0 or word.count("n't") > 0:
#         count += 1
#         print count, word, S140Bigram[word]
#
# for word in S140Pairgram:
#     if word.count("no") > 0 or word.count("not") > 0 or word.count("n't") > 0:
#         count += 1
#         print count, word, S140Pairgram[word]

# trainDependencies, testDependencies = loadSentenceDependency()
# cnt = 0
# for dpd in trainDependencies:
#     cnt += 1
#     print dpd
#     # S140vec = findContextFeature(dpd, S140Unigram)
#     # NRCvec = findContextFeature(dpd, NRCUnigram)
#     # print S140vec, NRCvec
#     if cnt > 20:
#         exit(0)
# word = "@gwg"
# if not (word.startswith("@") or word.startswith("http://")):
#     print word
#
# word = "http://fwefqwe"
# if not (word.startswith("@") or word.startswith("http://")):
#     print word
#
# word = "GW23EW"
# if not (word.startswith("@") or word.startswith("http://")):
#     print word
#
# print word.lower()
for i in xrange(1, 4):
    print i