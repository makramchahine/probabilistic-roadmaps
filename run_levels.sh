#!/bin/bash

# Loop over the values of nodes
# for nodes in 16 22 28 32 40 50 57 64 75 91 113 128 150 181 216 256 302 362 432 512 603 724 868 1024 ; do
for nodes in 32 64 128 256 512 1024 ; do
    # Loop over the values of level
    for level in 1; do
        # Run the command with the current values of nodes and level
        python prm_vs_samplers.py --obstacles --nodes $nodes --level $level -s --radius 6 --reps 50
    done
done

# Loop over the values of nodes
for nodes in 32 64 128 256 512 1024 ; do
    # Loop over the values of level
    for level in 2; do
        # Run the command with the current values of nodes and level
        python prm_vs_samplers.py --obstacles --nodes $nodes --level $level -s --radius 6 --reps 50
    done
done

# Loop over the values of nodes
for nodes in 64 128 256 512 1024 ; do
    # Loop over the values of level
    for level in 3; do
        # Run the command with the current values of nodes and level
        python prm_vs_samplers.py --obstacles --nodes $nodes --level $level -s --radius 6 --reps 50
    done
done
