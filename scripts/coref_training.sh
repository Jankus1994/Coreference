#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

> vectors.txt
list="list"
ls train/*.out.conllu > $list
while read name
do
    udapy read.Conllu files=$name demo.Coreference.CoNLL.Conll_feature_printer >> vectors.txt
done < $list
python3 ../udapi/block/demo/Coreference/Other/trainer.py $1 vectors.txt
