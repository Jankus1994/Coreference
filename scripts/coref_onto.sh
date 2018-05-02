#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

lang=$1
onf_list="$lang"_onf_list
txt_list="$lang"_txt_list
in_list="$lang"_in_list
out_list="$lang"_out_list

ls "$lang"_train/*.onf > $onf_list
cat $onf_list | sed 's/.onf/.txt/' > $txt_list
cat $onf_list | sed 's/.onf/.out.conllu/' > $out_list

python3 ../udapi/block/demo/Coreference/OntoNotes/onto_text_converter.py $onf_list $txt_list
udapy read.Sentences files="@$txt_list" udpipe.En demo.Coreference.OntoNotes.Onto_coref_conversion write.Conllu files="@$out_list"

ls "$lang"_test/*.onf > $onf_list
cat $onf_list | sed 's/.onf/.txt/' > $txt_list
cat $onf_list | sed 's/.onf/.in.conllu/' > $in_list
cat $onf_list | sed 's/.onf/.out.conllu/' > $out_list

python3 ../udapi/block/demo/Coreference/OntoNotes/onto_text_converter.py $onf_list $txt_list
udapy read.Sentences files="@$txt_list" udpipe.En write.Conllu files="@$in_list"
udapy read.Conllu files="@$in_list" demo.Coreference.OntoNotes.Onto_coref_conversion write.Conllu files="@$out_list"

