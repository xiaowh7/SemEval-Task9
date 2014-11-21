__author__ = 'seven'
filename = "SemEval2014-task9-test-B-gold_reformated.txt"
file = open(filename, 'r')
for line in file:
    data = line.strip('\r\n').split('\t')
    source = data[1]
    if not (source.startswith("SM") or source.startswith("T13")
        or source.startswith("T14") or source.startswith("LJ")):
        print source
