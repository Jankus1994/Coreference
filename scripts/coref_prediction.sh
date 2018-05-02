#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

lang=$1
in_list="$lang"_in_list
auto_list="$lang"_auto_list

ls "$lang"_test/*.in.conllu > $in_list
cat $in_list | sed 's/.in.conllu/.auto.conllu/' > $auto_list

#while read name
#do
  #  file="$lang"_test/$name.in.conllu
    #auto="$lang"_test/$name.auto.conllu
    #udapy read.Conllu files=$file demo.Coreference.CoNLL.Conll_prediction rel_model=rel_"$lang"_model dem_model=dem_"$lang"_model prs_model=prs_"$lang"_model prodrop_model=prodrop_"$lang"_model write.Conllu > $auto
#done < $list
#rm $list

udapy read.Conllu files="@$in_list" demo.Coreference.CoNLL.Conll_prediction rel_model=rel_"$lang"_model dem_model=dem_"$lang"_model prs_model=prs_"$lang"_model prodrop_model=prodrop_"$lang"_model write.Conllu files="@$auto_list"
