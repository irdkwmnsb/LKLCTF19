#!/bin/bash
for i in {1..20}; do
    echo starting $i;
    (python3 solve.py $*; echo $i done.) &
done;