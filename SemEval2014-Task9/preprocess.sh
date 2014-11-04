#!/bin/bash
python preprocess.py \
SemEval2014-task9-test-B-gold.txt \
SemEval2014-task9-test-B-gold_reformated.txt \
tweets.txt 
../ark-tweet-nlp/twokenize.sh tweets.txt | sed -n 's/\t.*$//gw tokens.txt'
./dependencyParser.sh
