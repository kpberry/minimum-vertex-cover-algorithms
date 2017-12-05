#!/usr/bin/env bash
# File for running all hill climbing tests.
# Splits the data into batches of 4 so that each run can be executed in
# parallel on my dual core machine without significant loss of performance.
for algo in LS1;
do
    mkdir ${algo}
    for filename in ./data/Data/*.graph; do
        for ((i=0;i<4;i+=1))
        do
            echo ${filename}
            echo ${algo}
            python3 main.py -inst ${filename} -alg ${algo} -seed $i -time 600 &
        done
        sleep 630
        mv *.trace *.sol ${algo}/
    done
    mkdir ${algo}
    for filename in ./data/Data/*.graph; do
        for ((i=4;i<8;i+=1))
        do
            echo ${filename}
            echo ${algo}
            python3 main.py -inst ${filename} -alg ${algo} -seed $i -time 600 &
        done
        sleep 630
        mv *.trace *.sol ${algo}/
    done
    mkdir ${algo}
    for filename in ./data/Data/*.graph; do
        for ((i=8;i<12;i+=1))
        do
            echo ${filename}
            echo ${algo}
            python3 main.py -inst ${filename} -alg ${algo} -seed $i -time 600 &
        done
        sleep 630
        mv *.trace *.sol ${algo}/
    done
done
