#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

lang=$1
list="$lang"_filenames
ls "$lang"_test/*.out.conllu | sed 's:.*/\(.*\)\.out.*:\1:' > $list
#ls "$lang"_test/ln94200_45.out.conllu | sed 's:.*/\(.*\)\.out.*:\1:' > $list

python3 ../udapi/block/demo/Coreference/Other/evaluator.py $lang $list
