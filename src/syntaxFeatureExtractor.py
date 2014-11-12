from replaceExpand import *


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
                            totalScore += \
                                (score[phrase][positive] -
                                 score[phrase][negative])
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
    return [countEmoPos, countEmoNeg,
            isLastEmoPos, isLastEmoNeg,
            isFirstTokenEmoPos, isFirstTokenEmoNeg,
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

            if i == len(tweet) - 1:
                if word.count('?') > 0:
                    isLastQuestion = 1
                if word.count('!') > 0:
                    isLastExclamation = 1

    return [count['?'], count['!'],
            position['?'], position['!'],
            isLastExclamation, isLastQuestion]


def countPOStag(tweet, token):
    count = {'N': 0, 'V': 0, 'R': 0, 'P': 0, 'O': 0, 'A': 0}
    words = {'N': [], 'V': [], 'R': [], 'P': [], 'O': [], 'A': []}
    for i in range(len(tweet)):
        word = tweet[i].lower().strip(specialChar)
        # word=frozenset([tweet[i].lower().strip(specialChar)])
        if word:
            if token[i] in count:
                count[token[i]] += 1
                words[token[i]].append(word)
    return [count['N'], count['V'], count['R'],
            count['P'], count['O'], count['A']], \
           words


def findUrl(tweet, token):
    count = 0
    for i in range(len(tweet)):
        if token[i] == 'U':
            count += 1
    return [count]


def findFeatures(tweet, token,
                 stopWords, emoticonsDict, acronymDict, intensifiers):
    """takes as input the tweet and token and returns the feature vector"""

    tweet, token, \
    countAcronym, countRepetition, countHashtag, countURL, countTarget \
        = preprocesingTweet1(tweet, token, emoticonsDict, acronymDict)
    featureVector = []

    # number of each POS tag
    countPOStagVector, words = countPOStag(tweet, token)
    featureVector.extend(countPOStagVector)

    tweet, token, countNegation = preprocesingTweet2(tweet, token, stopWords)
    featureVector.extend(findCapitalised(tweet, token))
    featureVector.extend(findEmoticons(tweet, token, emoticonsDict))
    # featureVector.extend(findIntensifiers(tweet, token, intensifiers))
    # featureVector.extend(findUrl(tweet,token))

    # number of acronym
    featureVector.extend([countAcronym])
    # number of words which had repetion
    featureVector.extend([countRepetition])
    # number of negtation
    featureVector.extend([countNegation])
    # number of hashtag
    featureVector.extend([countHashtag])
    # number of preposition
    # featureVector.extend([countPreposition])
    # number of URL
    # featureVector.extend([countURL])
    # number of @
    # featureVector.extend([countTarget])
    # number of special char
    featureVector.extend(countSpecialChar(tweet))

    hashtags = findHashtag(tweet, token)

    return featureVector, words, hashtags, tweet