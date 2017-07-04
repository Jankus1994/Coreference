#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

udapy read.Conllu files='!*.out.conllu' demo.Coreference.CoNLL.Conll_selector | python ../udapi/block/demo/Coreference/Other/trainer.py model.txt
