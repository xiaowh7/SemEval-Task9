__author__ = 'seven'
def Semeval2014Output(predictLabel, goldFilename, predFilename):
    goldFile = open(goldFilename, 'r')
    predFile = open(predFilename, 'w')

    index = 0
    for line in goldFile:
        data = line.strip("\r\n").split("\t")
        predFile.write("%s\t%d\t%s\n" % (data[0], index+1, predictLabel[index]))
        index += 1

    goldFile.close()
    predFile.close()


def Semeval2013Output(predictLabel, goldFilename, predFilename):
    goldFile = open(goldFilename, 'r')
    predFile = open(predFilename, 'w')

    index = 0
    for line in goldFile:
        data = line.strip("\r\n").split("\t")
        predFile.write("%s\t%s\t%s\t%s\n" %
                       (data[0], data[1], predictLabel[index], data[3]))
        index += 1

    goldFile.close()
    predFile.close()