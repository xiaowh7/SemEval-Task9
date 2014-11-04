# from senti_classifier import senti_classifier
from replaceExpand import *


# def calculateScore(tweet, polarityDictionary):
#     score = {}
#     tweet = [i.lower().strip(specialChar) for i in tweet]
#     tweet = [i for i in tweet if i]
#     length = len(tweet)
#     init = 0
#     neutralScore = 0
#     while init < length:
#         for i in range(init, length):
#             flag = 0
#             for j in range(length, i, -1):
#                 phrase = frozenset(tweet[i:j])
#                 if phrase in polarityDictionary:
#                     init = j
#                     flag = 1
#                     posScore = polarityDictionary[phrase][positive]
#                     negScore = polarityDictionary[phrase][negative]
#                     neutralScore = polarityDictionary[phrase][neutral]
#                     score[phrase] = [posScore, negScore, neutralScore]
#                     break
#             if flag == 1:
#                 break
#             else:
#                 posScore, negScore = senti_classifier.polarity_scores([tweet[i]])
#                 score[frozenset([tweet[i]])] = [posScore, negScore, neutralScore]
#                 polarityDictionary[frozenset([tweet[i]])] = [posScore, negScore, neutralScore]
#     return score, polarityDictionary


def findCapitalised(tweet, token):
    count = 0
    countCap = 0
    for i in range(len(tweet)):
        if token[i] != '$':
            word = tweet[i].strip(specialChar)
            if word:
                count += 1
                if word.isupper():
                    countCap += 1

    return [countCap]


def findNegation(tweet):
    countNegation = 0
    for i in range(len(tweet)):
        if tweet[i] == 'negation':
            countNegation += 1
    return [countNegation]


def findTotalScore(score):
    totalScore = 0
    for i in score.values():
        totalScore += (i[positive] - i[negative])
    return [totalScore]


def findPositiveNegativeWords(tweet, token, score):
    countPos = 0
    countNeg = 0
    count = 0
    totalScore = 0
    if tweet:
        for i in range(len(tweet)):
            if token[i] not in listSpecialTag:
                word = frozenset([tweet[i].lower().strip(specialChar)])
                if word:
                    count += 1
                    for phrase in score.keys():
                        if word.issubset(phrase):
                            if score[phrase][positive] != 0.0:
                                countPos += 1
                            if score[phrase][negative] != 0.0:
                                countNeg += 1
                            totalScore += (score[phrase][positive] - score[phrase][negative])
    return [countPos, countNeg, totalScore]


def findIntensifiers(tweet, token, intensifiers):
    countIntensifier = 0

    for i in range(len(tweet)):
        if tweet[i] in intensifiers:
            token[i] = 'Intensifier'
            countIntensifier += 1

    return [countIntensifier]


def findEmoticons(tweet, token, emoDict):
    countEmoPos = 0
    countEmoNeg = 0
    isLastEmoPos = 0
    isLastEmoNeg = 0
    isLastTokenEmoPos = 0
    isLastTokenEmoNeg = 0
    isFirstTokenEmoPos = 0
    isFirstTokenEmoNeg = 0

    for i in range(len(tweet)):
        if token[i] == 'E':
            if tweet[i] in emoDict:

                emo = emoDict[tweet[i]]
                if emo == 'Extremely-Positive' or emo == 'Positive':
                    # countEmoExtremePos += 1
                    countEmoPos += 1
                    isLastEmoPos = 1
                    isLastEmoNeg = 0
                if emo == 'Extremely-Negative' or emo == 'Negative':
                    # countEmoExtremeENeg += 1
                    countEmoNeg += 1
                    isLastEmoPos = 0
                    isLastEmoNeg = 1

                if i == len(tweet) - 1:
                    # print "The last token is Emoticon %s" % emo
                    if emo == 'Extremely-Positive' or emo == 'Positive':
                        isLastTokenEmoPos = 1
                    if emo == 'Extremely-Negative' or emo == 'Negative':
                        isLastTokenEmoNeg = 1
                elif i == 0:
                    # print "The first token is Emoticon %s" % emo
                    if emo == 'Extremely-Positive' or emo == 'Positive':
                        isFirstTokenEmoPos = 1
                    if emo == 'Extremely-Negative' or emo == 'Negative':
                        isFirstTokenEmoNeg = 1
    return [countEmoPos, countEmoNeg, isLastEmoPos, isLastEmoNeg, isFirstTokenEmoPos, isFirstTokenEmoNeg,
            isLastTokenEmoPos, isLastTokenEmoNeg]


def findHashtag(tweet, token):
    count = 0
    hashtags = []
    for i in range(len(tweet)):
        if token[i] == '#':
            count += 1
            hashtag = tweet[i].strip(specialChar).lower()
            hashtags.append(hashtag)
    return hashtags


def countSpecialChar(tweet):
    count = {'?': 0, '!': 0}
    position = {'?': 0, '!': 0}
    max = {'?': 0, '!': 0}
    # contiguousSequence = {'??': 0, '!!': 0, '!?': 0, '?!': 0}
    isLastExclamation = 0
    isLastQuestion = 0
    # count={'?':[0,0],'!':[0,0],'*':[0,0]}
    for i in range(len(tweet)):
        word = tweet[i].lower().strip(specialChar)
        # word=frozenset([tweet[i].lower().strip(specialChar)])
        if word:
            for symbol in count:
                cnt = word.count(symbol)
                if cnt > 0:
                    count[symbol] += cnt
                    if count[symbol] == cnt:
                        position[symbol] = i
                    if cnt > max[symbol]:
                        max[symbol] = cnt

            # for symbol in contiguousSequence:
            #     contiguousSequence[symbol] += word.count(symbol)

            if i == len(tweet) - 1:
                if word.count('?') > 0:
                    isLastQuestion = 1
                if word.count('!') > 0:
                    isLastExclamation = 1

    # return [count['?'], count['!'], position['?'], position['!'], max['?'], max['!'], isLastExclamation, isLastQuestion]
    return [count['?'], count['!'], position['?'], position['!'], isLastExclamation, isLastQuestion]


def countPosTag(tweet, token):
    count = {'N': 0, 'V': 0, 'R': 0, 'P': 0, 'O': 0, 'A': 0}
    words = {'N': [], 'V': [], 'R': [], 'P': [], 'O': [], 'A': []}

    for i in range(len(tweet)):
        word = tweet[i].lower().strip(specialChar)
        # word=frozenset([tweet[i].lower().strip(specialChar)])
        if word:
            if token[i] in count:
                count[token[i]] += 1
                words[token[i]].append(word)

    return [count['N'], count['V'], count['R'], count['P'], count['O'], count['A']], words


# return [ count['N'][positive], count['V'][positive], count['R'][positive], count['P'][positive], count['O'][positive], count['A'][positive], count['N'][negative], count['V'][negative], count['R'][negative], count['P'][negative], count['O'][negative], count['A'][negative] ]

def findUrl(tweet, token):
    count = 0
    for i in range(len(tweet)):
        if token[i] == 'U':
            count += 1
    return [count]


# def findFeatures(tweet, token, polarityDictionary, stopWords, emoticonsDict, acronymDict):
#     """takes as input the tweet and token and returns the feature vector"""
#
#     tweet, token, countAcronym, countRepetition, countHashtag, countPreposition = preprocesingTweet1(tweet, token,
#                                                                                                      emoticonsDict,
#                                                                                                      acronymDict)
#     score, polarityDictionary = calculateScore(tweet, polarityDictionary)
#     featureVector = []
#     featureVector.extend(findTotalScore(score))
#     tweet, token, countNegation = preprocesingTweet2(tweet, token, stopWords)
#     featureVector.extend(findCapitalised(tweet, token))
#     featureVector.extend(findHashtag(tweet, token, score))
#     featureVector.extend(findEmoticons(tweet, token))
#     featureVector.extend(findNegation(tweet))
#     featureVector.extend(findPositiveNegativeWords(tweet, token, score))
#     # #featureVector.extend(findUrl(tweet,token))
#     featureVector.extend([countAcronym])  # number of acronym
#     featureVector.extend([countRepetition])  # number of words which had repetion
#     featureVector.extend([countNegation])  # number of negtation
#     featureVector.extend([countHashtag])  # number of hashtag
#     featureVector.extend([countPreposition])  # number of preposition
#     featureVector.extend(countSpecialChar(tweet))  # number of  special char
#
#     featureVector.extend(countPosTag(tweet, token))
#     # for line in featureVector:
#     #     print line
#     return featureVector, polarityDictionary


def findFeatures1(tweet, token, stopWords, emoticonsDict, acronymDict, intensifiers):
    """takes as input the tweet and token and returns the feature vector"""

    tweet, token, countAcronym, countRepetition, countHashtag, countURL, countTarget \
        = preprocesingTweet1(tweet, token, emoticonsDict, acronymDict)
    featureVector = []
    vec, words = countPosTag(tweet, token)
    featureVector.extend(vec)

    tweet, token, countNegation = preprocesingTweet2(tweet, token, stopWords)
    featureVector.extend(findCapitalised(tweet, token))
    featureVector.extend(findEmoticons(tweet, token, emoticonsDict))
    # featureVector.extend(findIntensifiers(tweet, token, intensifiers))
    # #featureVector.extend(findUrl(tweet,token))
    featureVector.extend([countAcronym])  # number of acronym
    featureVector.extend([countRepetition])  # number of words which had repetion
    featureVector.extend([countNegation])  # number of negtation
    featureVector.extend([countHashtag])  # number of hashtag
    # featureVector.extend([countPreposition])  # number of preposition
    # featureVector.extend([countURL])  # number of URL
    # featureVector.extend([countTarget])  # number of @
    # featureVector.extend(countPos)

    featureVector.extend(countSpecialChar(tweet))  # number of  special char

    hashtags = findHashtag(tweet, token)

    return featureVector, words, hashtags, tweet


def findWordgram(tweet, uniModel, biModel, triModel, f4Model):
    vector = []

    uniVector = [0] * len(uniModel)
    for i in tweet:
        word = i.strip(specialChar).lower()
        if word:
            if word in uniModel:
                ind = uniModel.index(word)
                uniVector[ind] = 1
    vector = vector + uniVector

    biVector = [0] * len(biModel)
    tweet = [i.strip(specialChar).lower() for i in tweet]
    tweet = [i for i in tweet if i]
    for i in range(len(tweet) - 1):
        phrase = tweet[i] + ' ' + tweet[i + 1]
        if phrase in biModel:
            ind = biModel.index(phrase)
            biVector[ind] = 1
    vector = vector + biVector

    triVector = [0] * len(triModel)
    tweet = [i.strip(specialChar).lower() for i in tweet]
    tweet = [i for i in tweet if i]
    for i in range(len(tweet) - 2):
        phrase = tweet[i] + ' ' + tweet[i + 1] + ' ' + tweet[i + 2]
        if phrase in triModel:
            ind = triModel.index(phrase)
            triVector[ind] = 1

        phrase = tweet[i] + ' ' + '*' + ' ' + tweet[i + 2]
        if phrase in triModel:
            ind = triModel.index(phrase)
            triVector[ind] = 1

    vector = vector + triVector

    f4Vector = [0] * len(f4Model)
    tweet = [i.strip(specialChar).lower() for i in tweet]
    tweet = [i for i in tweet if i]
    for i in range(len(tweet) - 3):
        phrase = tweet[i] + ' ' + tweet[i + 1] + ' ' + tweet[i + 2] + ' ' + tweet[i + 3]
        if phrase in f4Model:
            ind = f4Model.index(phrase)
            f4Vector[ind] = 1

        phrase = tweet[i] + ' ' + '*' + ' ' + tweet[i + 2] + ' ' + tweet[i + 3]
        if phrase in f4Model:
            ind = f4Model.index(phrase)
            f4Vector[ind] = 1

        phrase = tweet[i] + ' ' + tweet[i + 1] + ' ' + '*' + ' ' + tweet[i + 3]
        if phrase in f4Model:
            ind = f4Model.index(phrase)
            f4Vector[ind] = 1

    vector = vector + f4Vector

    return vector


def findChargram(tweet, Char3Model, Char4Model, Char5Model):
    vector = []

    char3Vector = [0] * len(Char3Model)
    for word in tweet:
        word = word.strip(specialChar).lower()
        if word:
            for index in xrange(len(word) - 2):
                seq = word[index:index + 3]
                if seq in Char3Model:
                    ind = Char3Model.index(seq)
                    char3Vector[ind] = 1
    vector = vector + char3Vector

    char4Vector = [0] * len(Char4Model)
    for word in tweet:
        word = word.strip(specialChar).lower()
        if word:
            for index in xrange(len(word) - 3):
                seq = word[index:index + 4]
                if seq in Char4Model:
                    ind = Char4Model.index(seq)
                    char4Vector[ind] = 1
    vector = vector + char4Vector

    char5Vector = [0] * len(Char5Model)
    for word in tweet:
        word = word.strip(specialChar).lower()
        if word:
            for index in xrange(len(word) - 4):
                seq = word[index:index + 5]
                if seq in Char5Model:
                    ind = Char5Model.index(seq)
                    char5Vector[ind] = 1
    vector = vector + char5Vector

    return vector


def findUniScore(tweet, unigram, vector):
    maxuniscore = 0
    lastuniscore = 0
    unicount = 0
    tmpUni = []

    posscore = 0
    negscore = 0
    posmax = 0
    negmax = 0
    poscnt = 0
    negcnt = 0
    poslast = 0
    neglast = 0
    for i in range(len(tweet)):
        phrase = tweet[i].strip(specialChar).lower()
        tmpUni.append(phrase)
        if phrase in unigram:
            # print phrase
            score = unigram[phrase]
            if score > 0:
                posscore += score
                poscnt += 1
                unicount += 1
                if score > posmax:
                    posmax = score
                if score > maxuniscore:
                    maxuniscore = score
                poslast = score
            elif score < 0:
                negscore += score
                negcnt += 1
                unicount += 1
                if abs(score) > negmax:
                    negmax = abs(score)
                if abs(score) > maxuniscore:
                    maxuniscore = abs(score)
                neglast = score

            lastuniscore = score
    posvec = [posscore, poscnt, poslast, posmax]
    negvec = [negscore, negcnt, neglast, -negmax]
    vec = [posscore + negscore, unicount, lastuniscore, maxuniscore]
    vector = vector + posvec + negvec + vec
    return vector, tmpUni


def findBiScore(tweet, bigram, vector):
    # bigram score
    maxbiscore = 0
    lastbiscore = 0
    bicount = 0
    tmpBi = []

    posscore = 0
    negscore = 0
    posmax = 0
    negmax = 0
    poscnt = 0
    negcnt = 0
    poslast = 0
    neglast = 0
    for i in range(len(tweet) - 1):
        phrase = tweet[i] + ' ' + tweet[i + 1]
        phrase = phrase.strip(specialChar).lower()
        tmpBi.append(phrase)
        # print phrase
        if phrase in bigram:
            score = bigram[phrase]
            # print phrase
            if score > 0:
                posscore += score
                poscnt += 1
                bicount += 1
                if score > posmax:
                    posmax = score
                if score > maxbiscore:
                    maxbiscore = score
                poslast = score
            elif score < 0:
                negscore += score
                negcnt += 1
                bicount += 1
                if abs(score) > negmax:
                    negmax = abs(score)
                if abs(score) > maxbiscore:
                    maxbiscore = abs(score)
                neglast = score

            lastbiscore = score
    posvec = [posscore, poscnt, poslast, posmax]
    negvec = [negscore, negcnt, neglast, -negmax]
    vec = [posscore + negscore, bicount, lastbiscore, maxbiscore]
    vector = vector + posvec + negvec + vec
    return vector, tmpBi


def findPairScore(tmpBi, tmpUni, pairgram, vector):
    # pair score
    lastPairscore = 0
    maxPairscore = 0
    Paircount = 0

    posscore = 0
    negscore = 0
    posmax = 0
    negmax = 0
    poscnt = 0
    negcnt = 0
    poslast = 0
    neglast = 0
    for i in range(len(tmpUni)):
        for j in range(len(tmpUni)):
            phrase = tmpUni[i] + '---' + tmpUni[j]
            if phrase in pairgram:
                score = pairgram[phrase]
                # print phrase
                if score > 0:
                    posscore += score
                    poscnt += 1
                    Paircount += 1
                    if score > posmax:
                        posmax = score
                    if score > maxPairscore:
                        maxPairscore = score
                    poslast = score
                elif score < 0:
                    negscore += score
                    negcnt += 1
                    Paircount += 1
                    if abs(score) > negmax:
                        negmax = abs(score)
                    if abs(score) > maxPairscore:
                        maxPairscore = abs(score)
                    neglast = score

                lastPairscore = score
    for i in range(len(tmpUni)):
        for j in range(len(tmpBi)):
            phrase = tmpUni[i] + '---' + tmpBi[j]
            if phrase in pairgram:
                score = pairgram[phrase]
                # print phrase
                if score > 0:
                    posscore += score
                    poscnt += 1
                    Paircount += 1
                    if score > posmax:
                        posmax = score
                    if score > maxPairscore:
                        maxPairscore = score
                    poslast = score
                elif score < 0:
                    negscore += score
                    negcnt += 1
                    Paircount += 1
                    if abs(score) > negmax:
                        negmax = abs(score)
                    if abs(score) > maxPairscore:
                        maxPairscore = abs(score)
                    neglast = score

                lastPairscore = score
    for i in range(len(tmpBi)):
        for j in range(len(tmpUni)):
            phrase = tmpBi[i] + '---' + tmpUni[j]
            if phrase in pairgram:
                score = pairgram[phrase]
                # print phrase
                if score > 0:
                    posscore += score
                    poscnt += 1
                    Paircount += 1
                    if score > posmax:
                        posmax = score
                    if score > maxPairscore:
                        maxPairscore = score
                    poslast = score
                elif score < 0:
                    negscore += score
                    negcnt += 1
                    Paircount += 1
                    if abs(score) > negmax:
                        negmax = abs(score)
                    if abs(score) > maxPairscore:
                        maxPairscore = abs(score)
                    neglast = score

                lastPairscore = score
    for i in range(len(tmpBi)):
        for j in range(len(tmpBi)):
            phrase = tmpBi[i] + '---' + tmpBi[j]
            if phrase in pairgram:
                score = pairgram[phrase]
                # print phrase
                if score > 0:
                    posscore += score
                    poscnt += 1
                    Paircount += 1
                    if score > posmax:
                        posmax = score
                    if score > maxPairscore:
                        maxPairscore = score
                    poslast = score
                elif score < 0:
                    negscore += score
                    negcnt += 1
                    Paircount += 1
                    if abs(score) > negmax:
                        negmax = abs(score)
                    if abs(score) > maxPairscore:
                        maxPairscore = abs(score)
                    neglast = score

                lastPairscore = score
    posvec = [posscore, poscnt, poslast, posmax]
    negvec = [negscore, negcnt, neglast, -negmax]
    vec = [posscore + negscore, Paircount, lastPairscore, maxPairscore]
    # print posvec + negvec + vec
    vector = vector + posvec + negvec + vec
    return vector


def findLexiconScore(tweet, unigram, bigram, pairgram):
    vector = []

    vector, tmpUni = findUniScore(tweet, unigram, vector)

    vector, tmpBi = findBiScore(tweet, bigram, vector)

    vector = findPairScore(tmpBi, tmpUni, pairgram, vector)

    # totalscore = posscore + negscore
    # vector = vector + [totalscore, count, maxscore]
    return vector


def findManualLexiconScore(tweet, dict):
    vector = []

    posscore = 0
    negscore = 0
    posmax = 0
    negmax = 0
    poscnt = 0
    negcnt = 0
    poslast = 0
    neglast = 0

    maxscore = 0
    lastscore = 0

    for i in range(len(tweet)):
        phrase = tweet[i].lower()
        if phrase in dict:
            # print phrase
            score = dict[phrase]
            if score > 0:
                posscore += score
                poscnt += 1
                # unicount += 1
                if score > posmax:
                    posmax = score
                if score > maxscore:
                    maxscore = score
                poslast = score
            elif score < 0:
                negscore += score
                negcnt += 1
                # unicount += 1
                if abs(score) > negmax:
                    negmax = abs(score)
                if abs(score) > maxscore:
                    maxscore = abs(score)
                neglast = score

            lastscore = score

        if not i == len(tweet) - 1:
            phrase = tweet[i] + '-' + tweet[i + 1]
            phrase = phrase.strip(specialChar).lower()
            if phrase in dict:
                # print phrase
                score = dict[phrase]
                if score > 0:
                    posscore += score
                    poscnt += 1
                    # unicount += 1
                    if score > posmax:
                        posmax = score
                    if score > maxscore:
                        maxscore = score
                    poslast = score
                elif score < 0:
                    negscore += score
                    negcnt += 1
                    # unicount += 1
                    if abs(score) > negmax:
                        negmax = abs(score)
                    if abs(score) > maxscore:
                        maxscore = abs(score)
                    neglast = score

                lastscore = score

    posvec = [posscore, poscnt, poslast, posmax]
    negvec = [negscore, negcnt, neglast, -negmax]
    vec = [posscore + negscore, poscnt + negcnt, lastscore, maxscore]
    vector = vector + posvec + negvec + vec
    return vector


def findAFINNScore(tweet, dict):
    vector = []

    posscore = 0
    negscore = 0
    posmax = 0
    negmax = 0
    poscnt = 0
    negcnt = 0
    poslast = 0
    neglast = 0

    maxscore = 0
    lastscore = 0

    for i in range(len(tweet)):
        phrase = tweet[i].strip(specialChar).lower()
        if phrase in dict:
            # print phrase
            score = dict[phrase]
            if score > 0:
                posscore += score
                poscnt += 1
                # unicount += 1
                if score > posmax:
                    posmax = score
                if score > maxscore:
                    maxscore = score
                poslast = score
            elif score < 0:
                negscore += score
                negcnt += 1
                # unicount += 1
                if abs(score) > negmax:
                    negmax = abs(score)
                if abs(score) > maxscore:
                    maxscore = abs(score)
                neglast = score

            lastscore = score

        if not i == len(tweet) - 1:
            phrase = tweet[i] + ' ' + tweet[i + 1]
            phrase = phrase.strip(specialChar).lower()
            if phrase in dict:
                # print phrase
                score = dict[phrase]
                if score > 0:
                    posscore += score
                    poscnt += 1
                    # unicount += 1
                    if score > posmax:
                        posmax = score
                    if score > maxscore:
                        maxscore = score
                    poslast = score
                elif score < 0:
                    negscore += score
                    negcnt += 1
                    # unicount += 1
                    if abs(score) > negmax:
                        negmax = abs(score)
                    if abs(score) > maxscore:
                        maxscore = abs(score)
                    neglast = score

                lastscore = score

    posvec = [posscore, poscnt, poslast, posmax]
    negvec = [negscore, negcnt, neglast, -negmax]
    vec = [posscore + negscore, poscnt + negcnt, lastscore, maxscore]
    vector = vector + posvec + negvec + vec
    return vector


def findContextFeature(dependencies, unigram, emoticonsDict):
    vector = []

    #for dependency type amod, advmod, tmod, vmod
    modifyPosscore = 0
    modifyNegscore = 0
    modifyCount = 0
    modifyMax = 0
    modifyLastscore = 0

    modifiedPosscore = 0
    modifiedNegscore = 0
    modifiedCount = 0
    modifiedMax = 0
    modifiedLastscore = 0

    #for dependency type conj, cc
    conjPosscore = 0
    conjNegscore = 0
    conjCount = 0
    conjMax = 0
    conjLastscore = 0

    copPosscore = 0
    copNegscore = 0
    copCount = 0
    copMax = 0
    copLastscore = 0

    for type in dependencies:
        if type == "amod" or type == "advmod":
            for dpd in dependencies[type]:
                ###########################################################
                #modify feature for type mod
                word1 = dpd[0].lower()
                #GET the score
                score = 0
                if word1 in unigram and not (word1.startswith("@") or word1.startswith("http://")):
                    score = unigram[word1]

                if score > 0:
                    modifyPosscore += score
                    modifyCount += 1
                    if score > modifyMax:
                        modifyMax = score
                elif score < 0:
                    modifyNegscore += score
                    modifyCount += 1
                    if abs(score) > modifyMax:
                        modifyMax = score

                    modifyLastscore = score
                    ############################################################

                    ###########################################################
                    #modified feature for type mod
                word2 = dpd[1].lower()
                #GET the score
                score = 0
                if word2 in unigram and not (word2.startswith("@") or word2.startswith("http://")):
                    score = unigram[word2]
                elif word2 in emoticonsDict:
                    emo = emoticonsDict[word2]
                    if emo == 'Extremely-Positive' or emo == 'Positive':
                        score = 5
                    if emo == 'Extremely-Negative' or emo == 'Negative':
                        score = -5

                if score > 0:
                    modifiedPosscore += score
                    modifiedCount += 1
                    if score > modifiedMax:
                        modifiedMax = score
                elif score < 0:
                    modifiedNegscore += score
                    modifiedCount += 1
                    if abs(score) > modifiedMax:
                        modifiedMax = score

                modifiedLastscore = score
                ############################################################

        if type == "conj" or type == "cc":
            for dpd in dependencies[type]:
                word1 = dpd[0].lower()
                word2 = dpd[1].lower()
                #get the score
                score = 0
                if word2 in unigram and not (word2.startswith("@") or word2.startswith("https://")):
                    score += unigram[word2]
                if word1 in unigram and not (word1.startswith("@") or word1.startswith("https://")):
                    score += unigram[word1]

                if score > 0:
                    conjPosscore += score
                    conjCount += 1
                    if score > conjMax:
                        conjMax = score
                elif score < 0:
                    conjNegscore += score
                    conjCount += 1
                    if abs(score) > conjMax:
                        conjMax = score

                conjLastscore = score

        # if type == "cop":
        #     for dpd in dependencies[type]:
        #         word2 = dpd[1].lower()
        #         # word2 = dpd[1].lower()
        #         #get the score
        #         score = 0
        #
        #         if word2 in unigram and not (word2.startswith("https://")):
        #             score += unigram[word2]
        #
        #         if score > 0:
        #             copPosscore += score
        #             copCount += 1
        #             if score > copMax:
        #                 copMax = score
        #         elif score < 0:
        #             copNegscore += score
        #             copCount += 1
        #             if abs(score) > copMax:
        #                 copMax = score
        #
        #         copLastscore = score

    # modifyVec = [modifyPosscore, modifyNegscore, modifyCount, modifyMax, modifyLastscore]
    # modifiedVec = [modifiedPosscore, modifiedNegscore, modifiedCount, modifiedMax, modifiedLastscore]
    modifyVec = [modifyPosscore, modifyNegscore, modifyMax, modifyLastscore]
    modifiedVec = [modifiedPosscore, modifiedNegscore, modifiedMax, modifiedLastscore]
    conjVec = [conjPosscore, conjNegscore, conjMax, conjLastscore]
    # copVec = [copPosscore, copNegscore, copMax, copLastscore]
    # subjVec = [subjPosscore, subjNegscore, subjCount, subjMax, subjLastscore]
    # objVec = [objPosscore, objNegscore, objCount, objMax, objLastscore]
    # vector = vector + modifyVec + modifiedVec + subjVec + objVec
    vector = vector + modifyVec + modifiedVec + conjVec
    # print vector
    return vector


def findContextFeature1(dependencies, dict, intensifiers):
    #for dependency type neg
    isNegExist = 0

    rcmodScore = 0
    isRcmodExist = 0

    copScore = 0
    iscopExist = 0

    depScore = 0
    isDepExist = 0

    vector = []
    preByAdj = 0
    preByAdv = 0
    preByIntensifier = 0
    modifyStrSubj = 0
    modifyWeakSubj = 0
    modifiedStrSubj = 0
    modifiedWeakSubj = 0
    for type in dependencies:
        #get the feature preByAdj
        if type == "amod" or type == "acomp":
            preByAdj = 1

        #get the feature preByAdv
        if type == "advmod" or type == "advcl" or type == "npadvmod":
            preByAdv = 1

        #get the feature isNegExist
        if type == "neg":
            isNegExist = 1

        if type == "remod" or type == "acomp":
            isRcmodExist = 1
            for dpd in dependencies[type]:
                # word1 = dpd[0]
                word2 = dpd[1].lower()
                #get the score
                score = 0
                if word2 in dict:
                    score = dict[word2]
                if word2[-2:] == "ed":
                    word2_tmp = word2[:-1]
                    if word2_tmp in dict:
                        score += dict[word2]

                rcmodScore += score

        if type == "cop":
            iscopExist = 1

        if type == "dep":
            isdepExist = 1
            for dpd in dependencies[type]:
                word1 = dpd[0].lower()
                score = 0
                if word1 in dict:
                    score = dict[word1]

                depScore += score

        #get the feature preByIntensifier
        if type == "advmod":
            for dpd in dependencies[type]:
                word2 = dpd[1].lower()
                if word2 in intensifiers:
                    preByIntensifier = 1

        #get the feature modifyStrSubj, modifyWeakSubj, modifiedStrSubj,modifiedWeakSubj
        if type == "advmod" or type == "amod" or type == "partmod":
            for dpd in dependencies[type]:
                word1 = dpd[0].lower()
                word2 = dpd[1].lower()
                if word1 in dict:
                    score = dict[word1]
                    if score == 2 or score == (-2):
                        modifyStrSubj = 1
                    elif score == 1 or score == (-1):
                        modifyWeakSubj = 1

                if word2 in dict:
                    score == dict[word2]
                    if score == 2 or score == (-2):
                        modifiedStrSubj = 1
                    elif score == 1 or score == (-1):
                        modifiedWeakSubj = 1

    vector = [preByAdj, preByAdv, preByIntensifier, isNegExist]
    vector = vector + [modifyStrSubj, modifyWeakSubj, modifiedStrSubj, modifiedWeakSubj]
    vector = vector + [isRcmodExist, isDepExist, iscopExist]
    # vector = vector + [isRcmodExist, rcmodScore, isDepExist, depScore, iscopExist, copScore]
    # print vector
    return vector






