from itertools import izip

__author__ = 'seven'
import sys
import re


def reformat():
    if len(sys.argv) != 4:
        print "Usage :: python preprocess.py " \
              "InputFileName ReformatFileName OutputFileName"
        sys.exit(0)

    print ("Reformatting...")
    originFilename = "SemEval2014-Task9-subtaskAB-test-to-download/" \
                     "SemEval2014-task9-test-B-gold-NEED-TWEET-DOWNLOAD.txt"
    originFile = open(originFilename, 'r')

    infile = open(sys.argv[1], 'r')
    outfile = open(sys.argv[2], 'w')


    for line1, line2 in izip(infile, originFile):
        source = line1.split('\t')[1]
        if source.startswith("T13") or source.startswith("T14"):
            outfile.write("%s" % line1)
        else:
            outfile.write("%s" % line2)


def extractContent():
    p = re.compile("\\t(neutral|positive|negative)\\t.*$")

    print ("Extracting tweets...")
    infile = open(sys.argv[2], 'r')
    outfile = open(sys.argv[3], 'w')

    for line in infile:
        regs = p.search(line).regs
        start = regs[1][1] + 1
        end = regs[0][1]
        content = line[start:end]
        content = content.replace('\t', ' ')
        outfile.write("%s\n" % content)


if __name__ == "__main__":
    reformat()
    extractContent()