#!/usr/bin/env bash
for algo in BnB;
do
    mkdir ${algo}
    for filename in ./data/Data/*.graph;
    do
        echo ${filename}
        echo ${algo}
        python main.py -inst ${filename} -alg ${algo} -seed 0 -time 60
        mv *.trace *.sol ${algo}/
    done
done
