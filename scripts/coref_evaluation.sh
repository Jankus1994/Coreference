#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="filenames"

#ls test/*.out.conllu | sed 's:.*/\(.*\)\.out.*:\1:' > $list
#> eval
#while read name
#do
#    udapy read.Conllu files="test/$name.out.conllu test/$name.auto.conllu" demo.Coreference.CoNLL.Conll_evaluator >> eval
#done < $list
#python3 ../udapi/block/demo/Coreference/Other/finalizer.py eval

python3 ../udapi/block/demo/Coreference/Other/evaluator.py $list
