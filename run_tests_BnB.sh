#!/usr/bin/env bash
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
