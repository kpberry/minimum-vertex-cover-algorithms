#!/usr/bin/env bash
algo=LS1
mkdir ${algo}
for filename in ./data/Data/*.graph; do
    echo ${filename}
    python3 main.py -inst ${filename} -alg ${algo} -seed 0 -time 10
    mv *.trace *.sol ${algo}/
done