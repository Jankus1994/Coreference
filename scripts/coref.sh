#!/bin/bash

export PATH=../bin:$PATH
export PYTHONPATH=../:$PYTHONPATH

source py3env/bin/activate

# main file, processing od arguments
lang=$1
shift
if [ "$1" == 'p' ]; then
    sh coref_pdt.sh "$lang" # Pdt
    shift
else
    if [ "$1" == 'o' ]; then
        sh coref_onto.sh "$lang" # Ontonotes
        shift
    fi
fi

if [ "$1" == 't' ]; then
    sh coref_training.sh "$lang" # Training
    shift
fi

if [ "$1" == 'r' ]; then
    sh coref_prediction.sh "$lang" # pRediction (... Resolution)
    shift
fi

if [ "$1" == 'e' ]; then
    sh coref_evaluation.sh "$lang" # Evaluation
fi

deactivate
