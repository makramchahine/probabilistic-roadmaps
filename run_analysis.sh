#!/bin/bash

# Loop over the values of nodes
for nodes in 32 64 128; do
    # Loop over the values of level
    for level in 0 1 2; do
        # Run the command with the current values of nodes and level
        python analysis.py --nodes $nodes --level $level --reps 20 --plot
    done
done
