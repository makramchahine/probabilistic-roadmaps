# make a script that reads the level 3 csvs and plots the success rate of the different samplers on the same plot with the x axis being the number of nodes and the y axis being the success rate. The script should save the plot to a file called success_rate.png.

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from argparse import ArgumentParser

from config import SAMPLERS

# Level parse as argument
parser = ArgumentParser()
parser.add_argument('--level', type=int, default=3, help='Difficulty level of the environment')
args = parser.parse_args()

level = args.level

# root directory
root = f'/home/makramchahine/repos/PRM/results/analysis/level{level}/'

# find the nodes from the csv files names, it is the int after the first underscore
# e.g. summary_128_3.csv -> 128
nodes = []
for file in os.listdir(root):
    nodes.append(int(file.split('_')[1]))
# sort the nodes
nodes.sort()
# get rid of anything smaller than 64
# nodes = [n for n in nodes if n >= 64]

# convert to array
nodes = np.array(nodes)
# pow 2 nodes: get the nodes that are powers of 2
pow2 = np.log2(nodes) % 1 == 0
pow2 = nodes[pow2]

# samplers wihtout mpmc, sobol_unscr, halton_unscr, sukharev_add, tri_lat_add
# dists = SAMPLERS.copy()
# # dists.remove("mpmc")
# dists.remove("sobol_unscr")
# dists.remove("halton_unscr")
# dists.remove("sukharev_add")
# dists.remove("tri_lat_add")
# dists.remove("tri_lat")
# dists.remove("sukharev")

dists = ["uniform", "sobol_batch", "halton_batch", "mpmc_l2bat"]
# dists  = ["sobol_unscr", "halton_unscr", "mpmc_seq", "mpmc", "uniform"]

success_rates = np.zeros((len(nodes), len(dists)))

for i, n in enumerate(nodes):
    df = pd.read_csv(f'/home/makramchahine/repos/PRM/results/analysis/level{level}/summary_{n}_{level}.csv')
    for j, dist in enumerate(dists):
        try:
            success_rates[i, j] = 100 - df[dist][5]
        except:
            success_rates[i, j] = np.nan

print(success_rates)

valid_nodes = [32, 64, 128, 256, 512, 1024]

# Plot the success rates
plt.figure()
for i in range(len(dists)):
    # get the integer indices where the success rate is not nan
    mask = ~np.isnan(success_rates[:, i])

    if dists[i] in ["mpmc"]:
        # only plot mpmc for valid nodes
        mask = np.logical_and(mask, np.isin(nodes, valid_nodes))
    plt.plot(nodes[mask], success_rates[mask, i], label=dists[i], marker='o', alpha=0.35)

# plot a dashed line at 90% success rate
plt.axhline(90, color='black', linestyle='--')
# make x axis log scale
plt.xscale('log')
plt.xlabel('Number of Nodes')
# x ticks powers of two only, no subticks
plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter())
plt.gca().xaxis.set_major_locator(plt.FixedLocator([128, 256]))
plt.gca().xaxis.set_minor_locator(plt.NullLocator())
plt.gca().xaxis.set_minor_formatter(plt.NullFormatter())
plt.xticks(pow2, pow2)
plt.ylabel('Success Rate (%)')
# legend outside the plot above plot
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)
plt.savefig(f'SR_level{level}.png')
