#!/usr/bin/env bash
for algo in BnB;
do
    mkdir ${algo}
	mkdir pulp
    for filename in ./data/Data/*.graph;
    do
        echo ${filename}
        echo ${algo}
        python main.py -inst ${filename} -alg ${algo} -seed 0 -time 1800
        mv *.trace *.sol ${algo}/
		mv *.mps pulp/
    done
done
