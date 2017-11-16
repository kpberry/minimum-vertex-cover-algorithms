#!/usr/bin/env bash
for algo in BnB;
do
    mkdir ${algo}
    for filename in ./data/Data/*.graph; do
        for ((i=0;i<10;i+=1))
        do
            echo ${filename}
            echo ${algo}
            python main.py -inst ${filename} -alg ${algo} -seed $i -time 60
        done
        mv *.trace *.sol ${algo}/
    done
done
