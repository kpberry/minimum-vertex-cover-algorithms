#!/usr/bin/env bash
for algo in LS1 LS2;
do
    mkdir ${algo}
    for filename in ./data/Data/*.graph; do
        for ((i=0;i<10;i+=1))
        do
            echo ${filename}
            echo ${algo}
            python3 main.py -inst ${filename} -alg ${algo} -seed $i -time 600
        done
        mv *.trace *.sol ${algo}/
    done
done
