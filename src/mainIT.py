__author__ = 'seven'
"""This src extracts the features and returns the features"""
from featureExtractor import *
import sys
from classifier import *
from prepare import *
from svmutil import *

def findScore(words, vector):
    # find lexicon score for each word
    vec = []
    PosS140Vector, tmplist = findUniScore(words, S140Unigram, vec)
    vector = vector + PosS140Vector

    vec = []
    PosNRCVector, tmplist = findUniScore(words, NRCUnigram, vec)
    vector = vector + PosNRCVector

    PosLiuBingVector = findManualLexiconScore(words, LiuBingDict)
    vector = vector + PosLiuBingVector
    PosMPQAVector = findManualLexiconScore(words, MPQADict)
    vector = vector + PosMPQAVector
    PosNRCEmoticonVector = findManualLexiconScore(words, NRCEmotionDict)
    vector = vector + PosNRCEmoticonVector
    PosPosNegWordsVector = findManualLexiconScore(words, PosNegWords)
    vector = vector + PosPosNegWordsVector
    PosAFINNVector = findAFINNScore(words, AFINNDict)
    vector = vector + PosAFINNVector
    # print vector
    return vector


if __name__ == '__main__':

    """check arguments"""
    if len(sys.argv) != 3:
        print "Usage :: python mainDebate08.py ../dataset/finalTrainingInput.txt ../dataset/finalTestingInput"
        sys.exit(0)

    acronymDict, stopWords, emoticonsDict = loadDictionary()

    S140Unigram, S140Bigram, S140Trigram = loadS140Lexicon()
    NRCUnigram, NRCBigram, NRCTrigram = loanNRCLexicon()

    LiuBingDict = loadLiuBingLexicon()
    MPQADict = loadMPQALexicon()
    NRCEmotionDict = loadNRCEmoticonLexicon()
    PosNegWords = loadPosNegWords()
    AFINNDict = loadAFINNLexicon()
    # priorScore = dict(map(lambda (k, v): (
    #     frozenset(reduce(lambda x, y: x + y, [[i] if i not in acronymDict else acronymDict[i][0] for i in k.split()])),
    #     int(v)), [line.split('\t') for line in open("..//src//AFINN-111.txt")]))

    # for line in priorScore:
    #     print line, priorScore[line]
    # exit(0)
    uniModel, biModel, triModel, f4Model, Char3Model, Char4Model, Char5Model = loadNgram()

    # """ polarity dictionary combines prior score """
    # polarityDictionary = probTraining(priorScore)

    """write the polarityDictionary"""
    """
    data=[]
    for key in polarityDictionary:
        data.append(key+'\t'+str(polarityDictionary[key][positive])+'\t'+str(polarityDictionary[key][negative])+'\t'+str(polarityDictionary[key][neutral]))
    f=open('polarityDictionary.txt','w')
    f.write('\n'.join(data))
    f.close()
    """

    """Create a feature vector of training set """
    print "Creating Feature Vectors....."

    encode = {'positive': 1.0, 'negative': 2.0, 'neutral': 3.0}
    trainingLabel = []
    f = open(sys.argv[1], 'r')
    featureVectorsTrain = []
    for i in f:
        if i:
            i = i.split('\t')
            text = i[1]
            tweet = i[1].split()
            token = i[2].split()
            label = i[3].strip()
            if tweet:
                trainingLabel.append(encode[label])
                vector = []
                # vector, polarityDictionary = findFeatures(tweet, token, polarityDictionary, stopWords, emoticonsDict,
                #                                           acronymDict)
                vector, words, hashtags, tweet1 = findFeatures1(tweet, token, stopWords, emoticonsDict,
                                                          acronymDict)

                # find lexicon for each capitalised word
                # vector = findScore(capWords, vector)

                # find hashtag score for each hashtag
                vector = findScore(hashtags, vector)

                # find lexicon score for each pos-tags
                for pos in words:
                    vector = findScore(words[pos], vector)

                #find score for each lexicon
                chargramVector = findChargram(tweet, Char3Model, Char4Model, Char5Model)
                vector = vector + chargramVector

                wordgramVector = findWordgram(tweet, uniModel, biModel, triModel, f4Model)
                vector = vector + wordgramVector

                S140Vector = findLexiconScore(tweet, S140Unigram, S140Bigram, S140Trigram)
                vector.extend(S140Vector)

                NRCVector = findLexiconScore(tweet, NRCUnigram, NRCBigram, NRCTrigram)
                vector.extend(NRCVector)

                LiuBingVector = findManualLexiconScore(tweet, LiuBingDict)
                vector.extend(LiuBingVector)

                MPQAVector = findManualLexiconScore(tweet, MPQADict)
                vector.extend(MPQAVector)

                NRCEmotionVector = findManualLexiconScore(tweet, NRCEmotionDict)
                vector.extend(NRCEmotionVector)

                PosNegWordsVector = findManualLexiconScore(tweet, PosNegWords)
                vector.extend(PosNegWordsVector)

                AFINNVector = findAFINNScore(tweet, AFINNDict)
                vector.extend(AFINNVector)

                featureVectorsTrain.append(vector)
    f.close()
    print "Length of vector: %d" % len(featureVectorsTrain[0])
    print "Feature Vectors Train Created....."

    """for each new tweet create a feature vector and feed it to above model to get label"""

    testingLabel = []
    data = []
    data1 = []
    f = open(sys.argv[2], 'r')
    featureVectorsTest = []
    for i in f:
        if i:
            i = i.split('\t')
            text = i[1]
            tweet = i[1].split()
            token = i[2].split()
            label = i[3].strip()
            if tweet:
                data.append(label)
                testingLabel.append(encode[label])
                vector = []
                # vector, polarityDictionary = findFeatures(tweet, token, polarityDictionary, stopWords, emoticonsDict,
                #                                           acronymDict)
                vector, words, hashtags, tweet1 = findFeatures1(tweet, token, stopWords, emoticonsDict,
                                                          acronymDict)
                # find lexicon for each capitalised word
                # vector = findScore(capWords, vector)

                # find hashtag score for each hashtag
                vector = findScore(hashtags, vector)

                # find lexicon score for each pos-tags
                for pos in words:
                    vector = findScore(words[pos], vector)

                # find score for each lexicon
                chargramVector = findChargram(tweet, Char3Model, Char4Model, Char5Model)
                vector = vector + chargramVector

                wordgramVector = findWordgram(tweet, uniModel, biModel, triModel, f4Model)
                vector = vector + wordgramVector

                S140Vector = findLexiconScore(tweet, S140Unigram, S140Bigram, S140Trigram)
                vector.extend(S140Vector)

                NRCVector = findLexiconScore(tweet, NRCUnigram, NRCBigram, NRCTrigram)
                vector.extend(NRCVector)

                LiuBingVector = findManualLexiconScore(tweet, LiuBingDict)
                vector.extend(LiuBingVector)

                MPQAVector = findManualLexiconScore(tweet, MPQADict)
                vector.extend(MPQAVector)

                NRCEmotionVector = findManualLexiconScore(tweet, NRCEmotionDict)
                vector.extend(NRCEmotionVector)

                PosNegWordsVector = findManualLexiconScore(tweet, PosNegWords)
                vector.extend(PosNegWordsVector)

                AFINNVector = findAFINNScore(tweet, AFINNDict)
                vector.extend(AFINNVector)
                # print len(vector)
                featureVectorsTest.append(vector)
    f.close()
    print "Length of vector: %d" % len(featureVectorsTest[0])
    print "Feature Vectors of test input created. Calculating Accuracy..."

    predictedLabel = svmClassifier(trainingLabel, testingLabel, featureVectorsTrain, featureVectorsTest)

    for i in range(len(predictedLabel)):
        givenLabel = predictedLabel[i]
        label = encode.keys()[encode.values().index(givenLabel)]
        data1.append(label)

    f = open('..//src//taskB.gs', 'w')
    f.write('\n'.join(data))
    f.close()

    f = open('..//src//taskB.pred', 'w')
    f.write('\n'.join(data1))
    f.close()

    #print len(featureVectorsTest)
    #print len(testingLabel)
    #print len(featureVectorsTrain)
    #print len(trainingLabel)

    #svmClassifier(trainingLabel,testingLabel,featureVectorsTrain,featureVectorsTest)
    #naiveBayesClassifier(trainingLabel,testingLabel,featureVectorsTrain,featureVectorsTest)