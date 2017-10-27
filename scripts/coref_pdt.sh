#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="pdt_list"

ls pdt_train/*.? | sed 's:.*/\(.*\)\..*:\1:' | sort -u > $list
while read name
do
    w_file="pdt_train/$name.w"
    txt_file="pdt_train/$name.txt"
    in_file="pdt_train/$name.in.conllu"
    out_file="pdt_train/$name.out.conllu"
    
    python3 ../udapi/block/demo/Coreference/PDT/pdt_text_converter.py $w_file $txt_file
    cat $txt_file | udapy read.Sentences udpipe.Cs write.Conllu > $in_file
    udapy read.Conllu files=$in_file demo.Coreference.PDT.Pdt_main write.Conllu > $out_file
done < $list
rm $list



ls pdt_test/* | sed 's:.*/\(.*\)\..*:\1:' | sort -u > $list
while read name
do
    w_file="pdt_test/$name.w"
    txt_file="pdt_test/$name.txt"
    pdt_in_file="pdt_test/$name.in.conllu"
    #conll_in_file="pdt_test/$name.in.conllu"
    out_file="pdt_test/$name.out.conllu"
    
    python3 ../udapi/block/demo/Coreference/PDT/pdt_text_converter.py $w_file $txt_file
    cat $txt_file | udapy read.Sentences udpipe.Cs write.Conllu > $pdt_in_file
    #cp $pdt_in_file $conll_in_file
    udapy read.Conllu files=$pdt_in_file demo.Coreference.PDT.Pdt_main write.Conllu > $out_file
done < $list
rm $list
