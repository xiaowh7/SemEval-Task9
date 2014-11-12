__author__ = 'seven'
"""This src extracts the features and returns the features"""
from syntaxFeatureExtractor import *
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

    # PosLiuBingVector = findManualLexiconScore(words, LiuBingDict)
    # vector = vector + PosLiuBingVector
    # PosMPQAVector = findManualLexiconScore(words, MPQADict)
    # vector = vector + PosMPQAVector
    # PosNRCEmoticonVector = findManualLexiconScore(words, NRCEmotionDict)
    # vector = vector + PosNRCEmoticonVector
    # PosPosNegWordsVector = findManualLexiconScore(words, PosNegWords)
    # vector = vector + PosPosNegWordsVector
    # PosAFINNVector = findAFINNScore(words, AFINNDict)
    # vector = vector + PosAFINNVector
    # print vector
    return vector


if __name__ == '__main__':

    """check arguments"""
    if len(sys.argv) != 3:
        print "Usage :: python mainDebate08.py ../dataset/finalTrainingInput.txt ../dataset/finalTestingInput"
        sys.exit(0)

    acronymDict, stopWords, emoticonsDict = loadDictionary()

    S140Unigram, S140Bigram, S140Pairgram = loadS140Lexicon()
    NRCUnigram, NRCBigram, NRCPairgram = loanNRCLexicon()

    LiuBingDict = loadLiuBingLexicon()
    MPQADict = loadMPQALexicon()
    NRCEmotionDict = loadNRCEmoticonLexicon()
    PosNegWords = loadPosNegWords()
    AFINNDict = loadAFINNLexicon()

    intensifiers = loadIntersifier()
    trainDependencies, testDependencies = loadSentenceDependency()

    # uniModel, biModel, triModel, f4Model, Char3Model, Char4Model, Char5Model = loadNgram()

    """Create a feature vector of training set """
    print "Creating Feature Vectors....."

    encode = {'positive': 1.0, 'negative': 2.0, 'neutral': 3.0}
    trainingLabel = []
    trainfile = open(sys.argv[1], 'r')
    featureVectorsTrain = []
    index = 0
    for i in trainfile:
        if i:
            i = i.split('\t')
            text = i[1]
            tweet = i[1].split()
            token = i[2].split()
            label = i[3].strip()
            dependency = trainDependencies[index]
            index += 1
            if tweet:
                trainingLabel.append(encode[label])
                vector = []
                # vector, polarityDictionary = findFeatures(tweet, token, polarityDictionary, stopWords, emoticonsDict,
                #                                           acronymDict)
                vector, words, hashtags, tweet = findFeatures1(tweet, token, stopWords, emoticonsDict,
                                                          acronymDict, intensifiers)

                #find context feature
                S140ContextVector = findContextFeature(dependency, S140Unigram, emoticonsDict)
                vector.extend(S140ContextVector)

                NRCContextVector = findContextFeature(dependency, NRCUnigram, emoticonsDict)
                vector.extend(NRCContextVector)

                MPQAContextVector = findContextFeature1(dependency, MPQADict, intensifiers)
                vector.extend(MPQAContextVector)
                # LiuBingContextVector = findContextFeature(dependency, LiuBingDict)
                # vector.extend(LiuBingContextVector)
                #
                # MPQAContextVector = findContextFeature(dependency, MPQADict)
                # vector.extend(MPQAContextVector)
                #
                # NRCEmotionContextVector = findContextFeature(dependency, NRCEmotionDict)
                # vector.extend(NRCEmotionContextVector)
                #
                # PosNegWordsContextVector = findContextFeature(dependency, PosNegWords)
                # vector.extend(PosNegWordsContextVector)
                #
                # AFINNContextVector = findContextFeature(dependency, AFINNDict)
                # vector.extend(AFINNContextVector)

                #find char and word gram feature
                # chargramVector = findChargram(tweet, Char3Model, Char4Model, Char5Model)
                # vector = vector + chargramVector
                #
                # wordgramVector = findWordgram(tweet, uniModel, biModel, triModel, f4Model)
                # vector = vector + wordgramVector


                # find lexicon for each capitalised word
                # vector = findScore(capWords, vector)

                # find hashtag score for each hashtag
                vector = findScore(hashtags, vector)

                # find lexicon score for each pos-tags
                tags = ['N', 'V', 'R', 'O', 'A']
                for pos in words:
                    if pos in tags:
                        vector = findScore(words[pos], vector)

                #find score for each lexicon
                S140Vector = findLexiconScore(tweet, S140Unigram, S140Bigram, S140Pairgram)
                vector.extend(S140Vector)

                NRCVector = findLexiconScore(tweet, NRCUnigram, NRCBigram, NRCPairgram)
                vector.extend(NRCVector)

                LiuBingVector = findManualLexiconScore(tweet, LiuBingDict)
                vector.extend(LiuBingVector)

                MPQAVector = findManualLexiconScore(tweet, MPQADict)
                vector.extend(MPQAVector)

                NRCEmotionVector = findManualLexiconScore(tweet, NRCEmotionDict)
                vector.extend(NRCEmotionVector)

                # PosNegWordsVector = findManualLexiconScore(tweet, PosNegWords)
                # vector.extend(PosNegWordsVector)

                AFINNVector = findAFINNScore(tweet, AFINNDict)
                vector.extend(AFINNVector)

                featureVectorsTrain.append(vector)
    trainfile.close()
    print "Length of vector: %d" % len(featureVectorsTrain[0])
    print "Feature Vectors Train Created....."

    """for each new tweet create a feature vector and feed it to above model to get label"""

    testingLabel = []
    data = []
    data1 = []
    testfile = open(sys.argv[2], 'r')
    featureVectorsTest = []
    index = 0
    for i in testfile:
        if i:
            i = i.split('\t')
            text = i[1]
            tweet = i[1].split()
            token = i[2].split()
            label = i[3].strip()
            dependency = testDependencies[index]
            index += 1
            if tweet:
                data.append(label)
                testingLabel.append(encode[label])
                vector = []
                # vector, polarityDictionary = findFeatures(tweet, token, polarityDictionary, stopWords, emoticonsDict,
                #                                           acronymDict)
                vector, words, hashtags, tweet = findFeatures1(tweet, token, stopWords, emoticonsDict,
                                                          acronymDict, intensifiers)

                #find context feature
                S140ContextVector = findContextFeature(dependency, S140Unigram, emoticonsDict)
                vector.extend(S140ContextVector)

                NRCContextVector = findContextFeature(dependency, NRCUnigram, emoticonsDict)
                vector.extend(NRCContextVector)

                MPQAContextVector = findContextFeature1(dependency, MPQADict, intensifiers)
                vector.extend(MPQAContextVector)

                # LiuBingContextVector = findContextFeature(dependency, LiuBingDict)
                # vector.extend(LiuBingContextVector)
                #
                # MPQAContextVector = findContextFeature(dependency, MPQADict)
                # vector.extend(MPQAContextVector)
                #
                # NRCEmotionContextVector = findContextFeature(dependency, NRCEmotionDict)
                # vector.extend(NRCEmotionContextVector)
                #
                # PosNegWordsContextVector = findContextFeature(dependency, PosNegWords)
                # vector.extend(PosNegWordsContextVector)
                #
                # AFINNContextVector = findContextFeature(dependency, AFINNDict)
                # vector.extend(AFINNContextVector)

                #find char and word gram feature
                # chargramVector = findChargram(tweet, Char3Model, Char4Model, Char5Model)
                # vector = vector + chargramVector
                #
                # wordgramVector = findWordgram(tweet, uniModel, biModel, triModel, f4Model)
                # vector = vector + wordgramVector


                # find lexicon for each capitalised word
                # vector = findScore(capWords, vector)

                # find hashtag score for each hashtag
                vector = findScore(hashtags, vector)

                # find lexicon score for each pos-tags
                tags = ['N', 'V', 'R', 'O', 'A']
                for pos in words:
                    if pos in tags:
                        vector = findScore(words[pos], vector)

                # find score for each lexicon
                S140Vector = findLexiconScore(tweet, S140Unigram, S140Bigram, S140Pairgram)
                vector.extend(S140Vector)

                NRCVector = findLexiconScore(tweet, NRCUnigram, NRCBigram, NRCPairgram)
                vector.extend(NRCVector)

                LiuBingVector = findManualLexiconScore(tweet, LiuBingDict)
                vector.extend(LiuBingVector)

                MPQAVector = findManualLexiconScore(tweet, MPQADict)
                vector.extend(MPQAVector)

                NRCEmotionVector = findManualLexiconScore(tweet, NRCEmotionDict)
                vector.extend(NRCEmotionVector)

                # PosNegWordsVector = findManualLexiconScore(tweet, PosNegWords)
                # vector.extend(PosNegWordsVector)

                AFINNVector = findAFINNScore(tweet, AFINNDict)
                vector.extend(AFINNVector)
                # print len(vector)
                featureVectorsTest.append(vector)
    testfile.close()
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