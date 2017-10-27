#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="list"

ls test/*.in.conllu | sed 's:.*/\(.*\).in.conllu:\1:' > $list
while read name
do
    file="test/$name.in.conllu"
    auto="test/$name.auto.conllu"
    udapy read.Conllu files=$file demo.Coreference.CoNLL.Conll_prediction_selector demo.Coreference.CoNLL.Conll_predictor
    # selection of feature of the predicted file
    
    udapy read.Conllu files=$file demo.Coreference.CoNLL.Conll_coref_adder write.Conllu > $auto # adding of coref information to the predicted file
done < $list
rm $list
