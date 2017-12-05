#!/usr/bin/env bash
# File for automatically generating all approximation test data.
algo=Approx
mkdir ${algo}
for filename in ./data/Data/*.graph; do
    echo ${filename}
    python3 main.py -inst ${filename} -alg ${algo} -seed 0 -time 600
    mv *.trace *.sol ${algo}/
done