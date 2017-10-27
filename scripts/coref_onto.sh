#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

list="onto_list"

#ls onto_train/*.onf | sed 's:.*/\(.*\).onf$:\1:' > $list
#cat rozdiel > $list
#while read name
#do
#    onf_file="onto_train/$name.onf"
#    txt_file="onto_train/$name.txt"
#    in_file="onto_train/$name.in.conllu"
#    out_file="onto_train/$name.out.conllu"
#    
#    #python3 ../udapi/block/demo/Coreference/OntoNotes/onto_text_converter.py $onf_file $txt_file
#    #cat $txt_file | udapy read.Sentences udpipe.En write.Conllu > $in_file
#    udapy read.Conllu files=$in_file demo.Coreference.OntoNotes.Onto_main write.Conllu > $out_file
#done < $list
#rm $list



ls onto_test/*.onf | sed 's:.*/\(.*\).onf$:\1:' > $list
while read name
do
    onf_file="onto_test/$name.onf"
    txt_file="onto_test/$name.txt"
    onto_in_file="onto_test/$name.in.conllu"
    #conll_in_file="test/$name.in.conllu"
    out_file="onto_test/$name.out.conllu"
    
    python3 ../udapi/block/demo/Coreference/OntoNotes/onto_text_converter.py $onf_file $txt_file
    cat $txt_file | udapy read.Sentences udpipe.En write.Conllu > $onto_in_file
    #cp $onto_in_file $conll_in_file
    udapy read.Conllu files=$onto_in_file demo.Coreference.OntoNotes.Onto_main write.Conllu > $out_file
done < $list
rm $list

# adding coreference information from onf files to conllu files
#udapy read.Conllu files='!onto_train/*.in.conllu' demo.Coreference.OntoNotes.Onto_main write.Conllu > train/all.out.conllu # training files with coreference
#cat onto_test/*.in.conllu > test/all.in.conllu # testing files without coreference
#udapy read.Conllu files='!onto_test/*.in.conllu' demo.Coreference.OntoNotes.Onto_main write.Conllu > test/all.out.conllu # testing files with coreference (for evaluation)
