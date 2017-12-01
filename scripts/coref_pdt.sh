#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="list"

ls train/*.? | sed 's:.*/\(.*\)\..*:\1:' | sort -u > $list
while read name
do
    w_file="train/$name.w"
    txt_file="train/$name.txt"
    out_file="train/$name.out.conllu"
    
    python3 ../udapi/block/demo/Coreference/PDT/pdt_text_converter.py $w_file $txt_file
    udapy read.Sentences files=$txt_file udpipe.Cs demo.Coreference.PDT.Pdt_conversion write.Conllu > $out_file
done < $list
rm $list



ls test/*.? | sed 's:.*/\(.*\)\..*:\1:' | sort -u > $list
while read name
do
    w_file="test/$name.w"
    txt_file="test/$name.txt"
    out_file="test/$name.out.conllu"
    
    python3 ../udapi/block/demo/Coreference/PDT/pdt_text_converter.py $w_file $txt_file
    udapy read.Sentences files=$txt_file udpipe.Cs demo.Coreference.PDT.Pdt_conversion write.Conllu > $out_file
done < $list
rm $list
