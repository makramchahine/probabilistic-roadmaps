#!/bin/bash

# Loop over the values of nodes
for nodes in 32 64 128 256; do
    # Loop over the values of level
    for level in 0 1 2 3; do
        # Run the command with the current values of nodes and level
        python prm_vs_samplers.py --obstacles --iteration 40 --nodes $nodes --level $level -s --radius 6
    done
done
