#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

udapy read.Conllu files='!train/*.out.conllu' demo.Coreference.CoNLL.Conll_training_selector > vectors.txt
python3 ../udapi/block/demo/Coreference/Other/trainer.py $1 vectors.txt
