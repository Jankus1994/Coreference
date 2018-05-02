#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

lang=$1
rel_vectors=rel_"$lang"_vectors.txt
dem_vectors=dem_"$lang"_vectors.txt
prs_vectors=prs_"$lang"_vectors.txt
prodrop_vectors=prodrop_"$lang"_vectors.txt

> $rel_vectors
> $dem_vectors
> $prs_vectors
> $prodrop_vectors

list="$lang"_list
ls "$lang"_train/*.out.conllu > $list

udapy read.Conllu files="@$list" demo.Coreference.CoNLL.Conll_rel_feature_printer >> $rel_vectors
udapy read.Conllu files="@$list" demo.Coreference.CoNLL.Conll_dem_feature_printer >> $dem_vectors
udapy read.Conllu files="@$list" demo.Coreference.CoNLL.Conll_prs_feature_printer >> $prs_vectors
udapy read.Conllu files="@$list" demo.Coreference.CoNLL.Conll_prodrop_feature_printer >> $prodrop_vectors

python3 ../udapi/block/demo/Coreference/Other/trainer.py rel_"$lang"_model $rel_vectors
python3 ../udapi/block/demo/Coreference/Other/trainer.py dem_"$lang"_model $dem_vectors
python3 ../udapi/block/demo/Coreference/Other/trainer.py prs_"$lang"_model $prs_vectors
python3 ../udapi/block/demo/Coreference/Other/trainer.py prodrop_"$lang"_model $prodrop_vectors
