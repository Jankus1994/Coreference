#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

# main file, processing od arguments
if [ "$1" == 'p' ]; then
    sh coref_pdt.sh # Pdt
    shift
else
    if [ "$1" == 'o' ]; then
        sh coref_onto.sh # Ontonotes
        shift
    fi
fi

if [ "$1" == 't' ]; then
    sh coref_training.sh cz_model # Training
    shift
fi

if [ "$1" == 'r' ]; then
    sh coref_prediction.sh cz_model # pRediction (... Resolution)
    shift
fi

if [ "$1" == 'e' ]; then
    sh coref_evaluation.sh # Evaluation
fi
