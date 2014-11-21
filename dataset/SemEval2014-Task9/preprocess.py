__author__ = 'seven'
import sys
import re


def reformat():
    if len(sys.argv) != 4:
        print "Usage :: python preprocess.py " \
              "InputFileName ReformatFileName OutputFileName"
        sys.exit(0)

    print ("Reformatting...")
    infile = open(sys.argv[1], 'r')
    outfile = open(sys.argv[2], 'w')

    for line in infile:
        source = line.split('\t')[1]
        if source.startswith("SM") or source.startswith("LJ"):
            if line.endswith("\tNot Available\n"):
                line = line.replace("\tNot Available", "")

        outfile.write("%s" % line)


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