__author__ = 'seven'
from replaceExpand import *


def output(gramDict, outfileName, threshold):
    gramList = []
    for i in gramDict.keys():
        count = reduce(lambda x, y: x + y, gramDict[i])
        if count >= 10:
            count *= 1.0
            pos = gramDict[i][positive] / count
            neg = gramDict[i][negative] / count
            neu = gramDict[i][neutral] / count
            if pos > threshold or neg > threshold or neu > threshold:
                l = [i, pos, neg, neu, count]
                gramList.append(l)
    gramList = sorted(gramList, key=lambda x: x[4], reverse=True)
    outfile = open(outfileName, 'w')
    for i in xrange(len(gramList)):
        if i > 0:
            outfile.write('\n')
        outfile.write("%s" % gramList[i][0])


def createChargram(dataset, seqLen=3, threshold=0.9):
    if dataset == "Semeval" or dataset == "SemEval2014" or \
        dataset == "semeval":
        infileName = "../SemEval2014-Task9/trainingInput.txt"
        outfileName = \
            "../requirement/ngram/Semeval/Semeval_%dChargram.txt" % seqLen
    elif dataset == "debate08":
        infileName = "../dataset/dabate08/trainingInput.txt"
        outfileName = \
            "../requirement/ngram/debate08/debate08_%dChargram.txt" % seqLen
    elif dataset == "Apoorv":
        infileName = "../dataset/Apoorv/trainingInput.txt"
        outfileName = \
            "../requirement/ngram/Apoorv/Apoorv_%dChargram.txt" % seqLen
    else:
        exit("Error: Wrong dataset\nPlease specify a valid dataset.")

    chargramDict = {}
    infile = open(infileName, 'r')
    for line in infile:
        if line:
            line = line.strip('\n').split('\t')
            tokens = line[1].split()
            label = line[3].strip()
            if tokens and line[1] != "Not Available":
                tokens = [i.strip(specialChar).lower() for i in tokens]
                tokens = [i for i in tokens if i]
                for token in tokens:
                    if len(token) > 3:
                        for i in xrange(len(token) - 2):
                            seq = token[i:i + seqLen]
                            if seq not in chargramDict:
                                chargramDict[seq] = [0, 0, 0]
                            chargramDict[seq][eval(label)] += 1

    infile.close()

    output(chargramDict, outfileName, threshold)


def createNgram(dataset, phraseLen, threshold=0.8):
    if phraseLen == 1:
        feature = "uni"
    elif phraseLen == 2:
        feature = "bi"
    elif phraseLen == 3:
        feature = "tri"
    elif phraseLen == 4:
        feature = "4"
    else:
        exit("Error: Wrong value for phrase length\n"
             "Please specify a valid n for ngram.")

    if dataset == "Semeval" or dataset == "SemEval2014" or \
        dataset == "semeval":
        infileName = "../SemEval2014-Task9/trainingInput.txt"
        outfileName = \
            "../requirement/ngram/Semeval/Semeval_%sgram.txt" % feature
    elif dataset == "debate08":
        infileName = "../dataset/dabate08/trainingInput.txt"
        outfileName = \
            "../requirement/ngram/debate08/debate08_%sgram.txt" % feature
    elif dataset == "Apoorv":
        infileName = "../dataset/Apoorv/trainingInput.txt"
        outfileName = \
            "../requirement/ngram/Apoorv/Apoorv_%sgram.txt" % feature
    else:
        exit("Error: Wrong dataset\nPlease specify a valid dataset.")

    ngramDict = {}
    infile = open(infileName, 'r')
    for line in infile:
        if line:
            line = line.strip('\n').split('\t')
            tokens = line[1].split()
            label = line[3].strip()
            if tokens and line[1] != "Not Available":
                tokens = [i.strip(specialChar).lower() for i in tokens]
                tokens = [i for i in tokens if i]

                if phraseLen == 1:
                    for i in range(len(tokens)):
                        phrase = tokens[i]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1
                elif phraseLen == 2:
                    for i in range(len(tokens) - 1):
                        phrase = tokens[i] + ' ' + tokens[i + 1]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1
                elif phraseLen == 3:
                    for i in range(len(tokens) - 2):
                        phrase = tokens[i] + ' ' + tokens[i + 1] + ' ' + \
                            tokens[i + 2]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1

                        phrase = tokens[i] + ' ' + '*' + ' ' + tokens[i + 2]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1
                elif phraseLen == 4:
                    for i in range(len(tokens) - 3):
                        phrase = tokens[i] + ' ' + tokens[i+1] + ' ' + \
                            tokens[i+2] + ' ' + tokens[i+3]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1

                        phrase = tokens[i] + ' ' + '*' + ' ' + \
                            tokens[i+2] + ' ' + tokens[i+3]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1

                        phrase = tokens[i] + ' ' + tokens[i+1] + ' ' + \
                            '*' + ' ' + tokens[i+3]
                        if phrase not in ngramDict:
                            ngramDict[phrase] = [0, 0, 0]
                        ngramDict[phrase][eval(label)] += 1
                else:
                    exit("Error: Wrong value for phrase length\n"
                         "Please specify a valid n for ngram.")

    infile.close()

    output(ngramDict, outfileName, threshold)


if __name__ == "__main__":
    dataset = "Semeval"
    print "Creating %s_3Chargram.txt..." % dataset
    createChargram(dataset, 3, 0.9)
    print "Creating %s_4Chargram.txt..." % dataset
    createChargram(dataset, 4, 0.9)
    print "Creating %s_5Chargram.txt..." % dataset
    createChargram(dataset, 5, 0.9)

    print "Creating %s_unigram.txt..." % dataset
    createNgram(dataset, 1, 0.8)
    print "Creating %s_bigram.txt..." % dataset
    createNgram(dataset, 2, 0.8)
    print "Creating %s_trigram.txt..." % dataset
    createNgram(dataset, 3, 0.8)
    print "Creating %s_4gram.txt..." % dataset
    createNgram(dataset, 4, 0.8)

    print "%s ngram created." % dataset
