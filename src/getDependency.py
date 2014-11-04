__author__ = 'seven'
import re

#return dependency in form (key: type, value: [word1, word2])
def getDependency(filename="../dataset/dependency_train.txt"):
    infile = open(filename, 'r')
    dependencies = []
    pattern = re.compile("[(),-]")
    for line in infile.readlines():
        dpds = line.strip('\t\n').split('\t')
        ans = {}
        for dpd in dpds:
            match = re.split(pattern, dpd)
            # print match
            word1, word2, type = match[1], match[3], match[0]
            # phrase = "%s %s" %(word1, word2)
            # print word1, word2, dependency
            if type not in ans:
                ans[type] = [[word1, word2]]
            else:
                ans[type].append([word1, word2])
        dependencies.append(ans)

    # print len(dependencies)
    return dependencies