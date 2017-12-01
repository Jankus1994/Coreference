#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="list"

ls test/*.in.conllu | sed 's:.*/\(.*\).in.conllu:\1:' > $list
#echo ln94202_37 > $list
while read name
do
    file="test/$name.in.conllu"
    auto="test/$name.auto.conllu"
    udapy read.Conllu files=$file demo.Coreference.CoNLL.Conll_prediction model=$1 write.Conllu > $auto
    #break
done < $list
rm $list
