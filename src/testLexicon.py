import sys
from replaceExpand import *
from collections import defaultdict

if __name__ == '__main__':

    inFile = open(
        '../../NRC-Canada/NRC-Hashtag-Sentiment-Lexicon-v0.1/NRC-Hashtag-Sentiment-Lexicon-v0.1/unigrams-pmilexicon.txt',
        'r')
    unigram = {}
    for line in inFile.readlines():
        raw = line.split('\t')
        phrase = raw[0]
        score = float(raw[1])
        unigram[phrase] = score
    inFile.close()

    inFile = open(
        '../../NRC-Canada/NRC-Hashtag-Sentiment-Lexicon-v0.1/NRC-Hashtag-Sentiment-Lexicon-v0.1/bigrams-pmilexicon.txt',
        'r')
    bigram = {}
    for line in inFile.readlines():
        raw = line.split('\t')
        phrase = raw[0]
        score = float(raw[1])
        bigram[phrase] = score
    inFile.close()

    inFile = open(
        '../../NRC-Canada/NRC-Hashtag-Sentiment-Lexicon-v0.1/NRC-Hashtag-Sentiment-Lexicon-v0.1/pairs-pmilexicon.txt',
        'r')
    pairgram = {}
    for line in inFile.readlines():
        raw = line.split('\t')
        phrase = raw[0]
        score = float(raw[1])
        pairgram[phrase] = score
    inFile.close()

    # count = 0
    # for line in pairgram:
    #     count += 1
    #     if count == 100:
    #         exit(0)
    #     print line, pairgram[line]

    # """create emoticons dictionary"""
    # f = open("emoticonsWithPolarity.txt", 'r')
    # data = f.read().split('\n')
    # emoticonsDict = {}
    # for i in data:
    #     if i:
    #         i = i.split()
    #         value = i[-1]
    #         key = i[:-1]
    #         for j in key:
    #             emoticonsDict[j] = value
    # f.close()
    #
    # #print emoticonsDict
    #
    # """create acronym dictionary"""
    # f = open("acronym_tokenised.txt", 'r')
    # data = f.read().split('\n')
    # acronymDict = {}
    # for i in data:
    #     if i:
    #         i = i.split('\t')
    #         word = i[0].split()
    #         token = i[1].split()[1:]
    #         key = word[0].lower().strip(specialChar)
    #         value = [j.lower().strip(specialChar) for j in word[1:]]
    #         acronymDict[key] = [value, token]
    # f.close()

    index = 0
    poscrc = 0
    negcrc = 0
    poscount = 0
    negcount = 0
    pospre = 0
    negpre = 0
    count = 0
    f = open('../dataset/final_test-gold-B_Input.txt', 'r')
    for line in f:
        if line:
            index += 1
            # print line
            line = line.strip('\n').split('\t')
            tweet = line[1].split()
            # token = i[2].split()
            label = line[3].strip()
            if tweet and not label == 'neutral':
                posscore = 0
                negscore = 0
                count += 1
                # tweet, token, count1, count2 = preprocesingTweet1(tweet, token, emoticonsDict, acronymDict)
                # tweet = [i.strip(specialChar).lower() for i in tweet]
                tweet = [i for i in tweet if i]
                #unigram score
                tmpUni = []
                tmpBi = []
                for i in range(len(tweet)):
                    phrase = tweet[i]
                    phrase = phrase.lower()
                    tmpUni.append(phrase)
                    if phrase in unigram:
                        # print phrase
                        score = unigram[phrase]
                        if score > 0:
                            posscore += score
                        elif score < 0:
                            negscore += score

                #bigram score
                for i in range(len(tweet) - 1):
                    phrase = tweet[i] + ' ' + tweet[i + 1]
                    phrase = phrase.lower()
                    tmpBi.append(phrase)
                    # print phrase
                    if phrase in bigram:
                        # print phrase
                        score = bigram[phrase]
                        if score > 0:
                            posscore += score
                        elif score < 0:
                            negscore += score

                #pair score
                for i in range(len(tmpUni)):
                    for j in range(len(tmpBi)):
                        phrase = tmpUni[i] + '---' + tmpBi[j]
                        if phrase in pairgram:
                            # print phrase
                            score = pairgram[phrase]
                            if score > 0.0:
                                posscore += score
                            elif score < 0.0:
                                negscore += score

                total = posscore+negscore
                print "Index: %d, Positive Score: %f, Negtive Score: %f, Total Score: %f, Label: %s" % (
                    index, posscore, negscore, total, label)

                if label == 'positive':
                    poscount += 1
                elif label == 'negative':
                    negcount += 1

                if total > 0:
                    pospre += 1
                    if label == 'positive':
                        poscrc += 1
                elif total < 0:
                    negpre += 1
                    if label == 'negative':
                        negcrc += 1
    print poscrc, pospre, poscount
    print "Positive, Precision: %f, Recall: %f, " % ( float(poscrc)/pospre, float(poscrc)/poscount )
    print negcrc, negpre, negcount
    print "Negative, Precision: %f, Recall: %f, " % ( float(negcrc)/negpre, float(negcrc)/negcount )
    f.close()