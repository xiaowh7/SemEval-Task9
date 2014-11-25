__author__ = 'seven'
from ngramFeatureExtractor import *
from lexiconFeatureExtractor import *
from syntaxFeatureExtractor import *
from contextFeatureExtractor import *
from classifier import *
from prepare import *
from output import *
from svmutil import *


def init(dataset):
    if dataset == "Semeval2014" or dataset == "SemEval2014" or \
                    dataset == "semeval2014" or dataset == "semeval":
        trainFilename = "../dataset/trainset/train.csv"
        testFilename = "../dataset/SemEval2014-Task9/" \
                       "SemEval2014_test.csv"
        trainDepFilename = "../dataset/trainset/train_dependency.txt"
        testDepFilename = "../dataset/SemEval2014-Task9/" \
                          "SemEval2014_test_dependency.txt"
        goldFilename = "..//SemEval2014-task9-scoring-script//" \
                           "SemEval2014-task9-test-B-gold.txt"
    elif dataset == "Twitter-2013" or dataset == "twitter-2013" or \
                    dataset == "twitter2013":
        trainFilename = "../dataset/trainset/train.csv"
        testFilename = "../dataset/SemEval2014-Task9/Twitter-2013/" \
                       "Twitter-2013_test.csv"
        trainDepFilename = "../dataset/trainset/train_dependency.txt"
        testDepFilename = "../dataset/SemEval2014-Task9/Twitter-2013/" \
                          "Twitter-2013_dependency.txt"
        goldFilename = "../dataset/SemEval2014-Task9/Twitter-2013/" \
                           "Twitter-2013_gold.csv"
    elif dataset == "Twitter-2014" or dataset == "twitter-2014" or \
                    dataset == "twitter2014":
        trainFilename = "../dataset/trainset/train.csv"
        testFilename = "../dataset/SemEval2014-Task9/Twitter-2014/" \
                       "Twitter-2014_test.csv"
        trainDepFilename = "../dataset/trainset/train_dependency.txt"
        testDepFilename = "../dataset/SemEval2014-Task9/Twitter-2014/" \
                          "Twitter-2014_dependency.txt"
        goldFilename = "../dataset/SemEval2014-Task9/Twitter-2014/" \
                           "Twitter-2014_gold.csv"
    elif dataset == "debate08":
        trainFilename = "../dataset/debate08/debate08_train.csv"
        testFilename = "../dataset/debate08/debate08_test.csv"
        trainDepFilename = "../dataset/debate08/debate08_train_dependency.txt"
        testDepFilename = "../dataset/debate08/debate08_test_dependency.txt"
    elif dataset == "Apoorv":
        trainFilename = "../dataset/Apoorv/Apoorv_train.csv"
        testFilename = "../dataset/Apoorv/Apoorv_test.csv"
        trainDepFilename = "../dataset/Apoorv/Apoorv_train_dependency.txt"
        testDepFilename = "../dataset/Apoorv/Apoorv_test_dependency.txt"
    else:
        exit("Error: Wrong dataset\nPlease specify a valid dataset.")

    return trainFilename, testFilename, \
           trainDepFilename, testDepFilename, goldFilename


def getScoreFeatureVector(words, vector):
    # find lexicon score for each word
    vec = []
    Sentiment140Vector, tmplist = findUniScore(words, S140Unigram, vec)
    vector = vector + Sentiment140Vector

    vec = []
    NRCHashtagVector, tmplist = findUniScore(words, NRCUnigram, vec)
    vector = vector + NRCHashtagVector

    LiuBingVector = findManualLexiconScore(words, LiuBingDict)
    vector = vector + LiuBingVector

    MPQAVector = findManualLexiconScore(words, MPQADict)
    vector = vector + MPQAVector

    NRCEmoticonVector = findManualLexiconScore(words, NRCEmotionDict)
    vector = vector + NRCEmoticonVector

    PosNegWordsDictVector = findManualLexiconScore(words, PosNegWordsDict)
    vector = vector + PosNegWordsDictVector

    AFINNVector = findAFINNScore(words, AFINNDict)
    vector = vector + AFINNVector
    # print vector
    return vector


def createFeatureVectors(datafile, dependencies):
    labels = []
    featureVectors = []
    index = 0
    infile = open(datafile, 'r')
    for line in infile:
        if line:
            content = line.split('\t')
            tweet = content[1].split()
            token = content[2].split()
            label = content[3].strip()
            dependency = dependencies[index]
            index += 1

            if tweet:
                labels.append(encode[label])
                vector, words, hashtags, tweet = \
                    findFeatures(tweet, token, stopwords, emoticonsDict,
                                 acronymDict, intensifiers)

                # find context feature
                S140ContextVector = \
                    findContextFeature(dependency, S140Unigram, emoticonsDict)
                vector.extend(S140ContextVector)

                NRCContextVector = \
                    findContextFeature(dependency, NRCUnigram, emoticonsDict)
                vector.extend(NRCContextVector)

                MPQAContextVector = \
                    findContextFeature1(dependency, MPQADict, intensifiers)
                vector.extend(MPQAContextVector)


                # find char and word gram feature
                # chargramVector = \
                # findChargram(tweet, _3CharModel, _4CharModel, _5CharModel)
                # vector = vector + chargramVector
                #
                # wordgramVector = \
                #     findWordgram(tweet, uniModel, biModel, triModel, f4Model)
                # vector = vector + wordgramVector


                # find lexicon for each capitalised word
                # vector = getScoreFeatureVector(capWords, vector)

                # find hashtag score for each hashtag
                vector = getScoreFeatureVector(hashtags, vector)

                # find lexicon score for each pos-tags
                tags = ['N', 'V', 'R', 'O', 'A']
                for pos in words:
                    if pos in tags:
                        vector = getScoreFeatureVector(words[pos], vector)

                # find score for each lexicon
                S140Vector = \
                    findAutomaticLexiconScore(
                        tweet, S140Unigram, S140Bigram, S140Pairs)
                vector.extend(S140Vector)

                NRCVector = \
                    findAutomaticLexiconScore(
                        tweet, NRCUnigram, NRCBigram, NRCPairs)
                vector.extend(NRCVector)

                LiuBingVector = findManualLexiconScore(tweet, LiuBingDict)
                vector.extend(LiuBingVector)

                MPQAVector = findManualLexiconScore(tweet, MPQADict)
                vector.extend(MPQAVector)

                NRCEmotionVector = \
                    findManualLexiconScore(tweet, NRCEmotionDict)
                vector.extend(NRCEmotionVector)

                PosNegWordsDictVector = \
                    findManualLexiconScore(tweet, PosNegWordsDict)
                vector.extend(PosNegWordsDictVector)

                AFINNVector = findAFINNScore(tweet, AFINNDict)
                vector.extend(AFINNVector)

                featureVectors.append(vector)
    infile.close()
    return labels, featureVectors


if __name__ == '__main__':

    """check arguments"""
    if len(sys.argv) != 2:
        print "Usage :: python main.py SemEval2014"
        sys.exit("Error: wrong arguments")
    else:
        dataset = sys.argv[1]
        encode = {'positive': 1.0, 'negative': 2.0, 'neutral': 3.0}
        decode = {1.0: 'positive', 2.0: 'negative', 3.0: 'neutral'}
        trainFilename, testFilename, \
            trainDepFilename, testDepFilename, goldFilename = \
            init(dataset)
        goldStandard = []
        predictLabel = []
        # unigramModel, bigramModel, trigramModel, _4gramModel, \
        # _3ChargramModel, _4ChargramModel, _5ChargramModel = \
        # loadNgram(dataset)

    acronymDict, emoticonsDict = loadDictionary()
    stopwords, intensifiers = loadOtherReferences()

    S140Unigram, S140Bigram, S140Pairs = loanNRCCanadaLexicon("Sentiment140")
    NRCUnigram, NRCBigram, NRCPairs = loanNRCCanadaLexicon("NRC-Hashtag")

    LiuBingDict = loadLiuBingLexicon()
    MPQADict = loadMPQALexicon()
    NRCEmotionDict = loadNRCEmoticonLexicon()
    PosNegWordsDict = loadPosNegWords()
    AFINNDict = loadAFINNLexicon()

    trainDependencies, testDependencies = \
        loadDependency(trainDepFilename, testDepFilename)

    """Create feature vectors of training set """
    print "\n"
    print "Creating feature vectors for trainset..."
    trainLabel, trainFeatureVectors = \
        createFeatureVectors(trainFilename, trainDependencies)
    print "Length of feature vector for trainset: %d" \
          % len(trainFeatureVectors[0])
    print "Feature vectors of trainset created."

    """Create feature vectors of testset """
    print "Creating feature vectors for testset..."
    testLabel, testFeatureVectors = \
        createFeatureVectors(testFilename, testDependencies)

    print "Length of feature vector for testset: %d" \
          % len(testFeatureVectors[0])
    print "Feature vectors of testset created."

    for i in range(len(testLabel)):
        goldStandard.append(decode[testLabel[i]])

    encodePredictLabel = svmClassifier(
        trainLabel, testLabel, trainFeatureVectors, testFeatureVectors)

    # print predictLabel[1:10]
    for i in range(len(encodePredictLabel)):
        predictLabel.append(decode[encodePredictLabel[i]])

    f = open('..//src//taskB.pred', 'w')
    f.write('\n'.join(predictLabel))
    f.close()

    if dataset.startswith("Twitter"):
        predFilename = "../dataset/SemEval2014-Task9/%s/%s_pred.csv" \
                       % (dataset, dataset)
        Semeval2013Output(predictLabel, goldFilename, predFilename)
    else:
        predFilename = "../result/%s.pred" % dataset
        Semeval2014Output(predictLabel, goldFilename, predFilename)

