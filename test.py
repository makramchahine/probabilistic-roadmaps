# make a script that reads the level 3 csvs and plots the success rate of the different samplers on the same plot with the x axis being the number of nodes and the y axis being the success rate. The script should save the plot to a file called success_rate.png.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import SAMPLERS

# Load the csv files
nodes = [128, 181, 256, 362, 512, 724, 1024]
# convert to array
nodes = np.array(nodes)
# pow 2 nodes: get the nodes that are powers of 2
pow2 = np.log2(nodes) % 1 == 0
pow2 = nodes[pow2]

# samplers wihtout mpmc, sobol_unscr, halton_unscr, sukharev_add, tri_lat_add
dists = SAMPLERS.copy()
dists.remove("mpmc")
dists.remove("sobol_unscr")
dists.remove("halton_unscr")
dists.remove("sukharev_add")
dists.remove("tri_lat_add")

# dists = ["uniform", "sobol_scram", "halton_scram", "mpmc_rand"]

success_rates = np.zeros((len(nodes), len(dists)))

for i, n in enumerate(nodes):
    df = pd.read_csv(f'/home/makramchahine/repos/PRM/results/analysis/level3/summary_{n}_1_3.csv')
    for j, dist in enumerate(dists):
        try:
            success_rates[i, j] = 100 - df[dist][5]
        except:
            success_rates[i, j] = np.nan

print(success_rates)

# Plot the success rates
plt.figure()
for i in range(len(dists)):
    # get the integer indices where the success rate is not nan
    mask = ~np.isnan(success_rates[:, i])
    plt.plot(nodes[mask], success_rates[mask, i], label=dists[i], marker='o')
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
plt.savefig('success_rate.png')
