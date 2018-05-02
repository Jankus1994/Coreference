#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

lang=$1
w_list="$lang"_w_list
txt_list="$lang"_txt_list
in_list="$lang"_in_list
out_list="$lang"_out_list

ls "$lang"_train/*.w > $w_list
cat $w_list | sed 's/.w/.txt/' > $txt_list
cat $w_list | sed 's/.w/.out.conllu/' > $out_list

python3 ../udapi/block/demo/Coreference/PDT/pdt_text_converter.py $w_list $txt_list
udapy read.Sentences files="@$txt_list" udpipe.Cs demo.Coreference.PDT.Pdt_coref_conversion write.Conllu files="@$out_list"

ls "$lang"_test/*.w > $w_list
cat $w_list | sed 's/.w/.txt/' > $txt_list
cat $w_list | sed 's/.w/.in.conllu/' > $in_list
cat $w_list | sed 's/.w/.out.conllu/' > $out_list

python3 ../udapi/block/demo/Coreference/PDT/pdt_text_converter.py $w_list $txt_list
udapy read.Sentences files="@$txt_list" udpipe.Cs write.Conllu files="@$in_list"
udapy read.Conllu files="@$in_list" demo.Coreference.PDT.Pdt_coref_conversion write.Conllu files="@$out_list"
