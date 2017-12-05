#!/usr/bin/env bash
# File for running all branch and bound tests.
# Splits the data into batches of 4 so that each run can be executed in
# parallel on my dual core machine without significant loss of performance.
for algo in BnB;
do
    mkdir ${algo}
    count=0
    time=3600
    sleeptime=$((${time} + 30))
    for filename in ./data/Data/*.graph;
    do
        echo ${filename}
        echo ${algo}
        python3 main.py -inst ${filename} -alg ${algo} -seed 0 -time ${time} > out.txt &
        count=$((${count} + 1))
        if ((${count} % 4 == 0))
        then
            sleep ${sleeptime}
            mv *.trace *.sol ${algo}/
        fi
    done
done
