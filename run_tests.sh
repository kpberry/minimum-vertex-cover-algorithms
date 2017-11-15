#!/usr/bin/env bash
for filename in ./data/Data/*.graph; do
    echo $filename & python3 main.py -inst $filename -alg LS1 -seed 0 -time 30 &
done
