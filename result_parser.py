import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def parse_csv_files(directory):
    # Data structure to hold the parsed data
    data = defaultdict(lambda: defaultdict(dict))

    # Iterate over all CSV files in the directory sorted by filename
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".csv"):
            # Extract level and points from the filename (assuming filename format: "summary_points_iterations_level.csv")
            parts = filename.replace(".csv", "").split("_")
            level = int(parts[3])
            points = int(parts[1])

            # Read the CSV file and store data in the structure
            with open(os.path.join(directory, filename), mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Read the header row

                for row in reader:
                    metric = row[0]
                    metrics = {
                        'sobol_scram': float(row[1]),
                        'sobol_unscr': float(row[2]),
                        'uniform': float(row[3]),
                        'mpmc': float(row[4]),
                        'halton_unscr': float(row[5]),
                        'halton_scram': float(row[6]),
                        'tri_lat': float(row[7]),
                        'sukharev': float(row[8])
                    }

                    # Store data
                    data[level][points][metric] = metrics

    return data


# Example usage
directory = "/home/makramchahine/repos/PRM/results/analysis"
data = parse_csv_files(directory)

# Rearrange data structure
def rearrange_data(data, metric_type):
    s_data = defaultdict(lambda: defaultdict(dict))
    for level, points_data in data.items():
        for points, metrics in points_data.items():
            try:
                s_data[f'level_{level}'][points] = {
                    distrib: {
                        'average': metrics[f'average_{metric_type}'][distrib],
                        'std_dev': metrics[f'std_dev_{metric_type}'][distrib]
                    }
                    for distrib in distribs
                }
            except:
                s_data[f'level_{level}'][points] = {
                    distrib: metrics[metric_type][distrib]
                    for distrib in distribs
                }
    return s_data

distribs = ['sobol_scram', 'sobol_unscr', 'uniform', 'mpmc', 'halton_unscr', 'halton_scram', 'tri_lat', 'sukharev']

# Plot Cardinality
cardinality_data = rearrange_data(data, 'cardinality')

# Creating a bar plot for Cardinality with standard deviation, with a log base 2 scale for the y-axis
fig, ax = plt.subplots(figsize=(24, 8))

# Test levels and corresponding data
levels = list(cardinality_data.keys())
nodes = sorted(list(cardinality_data[levels[0]].keys()))

bar_width = 0.03  # Width of the bars
group_width = bar_width * len(levels)  # Total width of all bars in a group

# Define color palettes for each distrib
greens = plt.cm.Greens(np.linspace(0.3, 0.8, len(levels)))
blues = plt.cm.Blues(np.linspace(0.3, 0.8, len(levels)))
oranges = plt.cm.Oranges(np.linspace(0.3, 0.8, len(levels)))
purples = plt.cm.Purples(np.linspace(0.3, 0.8, len(levels)))
reds = plt.cm.Reds(np.linspace(0.3, 0.8, len(levels)))
grays = plt.cm.Greys(np.linspace(0.3, 0.8, len(levels)))
coppers = plt.cm.copper(np.linspace(0.3, 0.8, len(levels)))[::-1]
pinks = plt.cm.pink(np.linspace(0.3, 0.8, len(levels)))[::-1]


color_palettes = {
    'mpmc': greens,
    'sobol_scram': blues,
    'sobol_unscr': purples,
    'uniform': oranges,
    'halton_unscr': reds,
    'halton_scram': grays,
    'tri_lat': coppers,
    'sukharev': pinks
}

# Plotting each distrib separately
for i, distrib in enumerate(distribs):
    for j, level in enumerate(levels):
        avg_values = [cardinality_data[level][node][distrib]['average'] for node in nodes]
        std_dev_values = [cardinality_data[level][node][distrib]['std_dev'] for node in nodes]

        # Plotting the bars with standard deviation as error bars
        x = [pos + (i * len(levels) + j) * bar_width for pos in range(len(nodes))]
        color = color_palettes[distrib][j]
        ax.bar(x, avg_values, yerr=std_dev_values, width=bar_width, label=f"{distrib} {level}", color=color)

# Adding labels
ax.set_xlabel('Number of Nodes')
ax.set_ylabel('Cardinality (log2 scale)')
ax.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax.set_xticklabels(nodes)
ax.set_yticks([2**i for i in range(4,9)])
ax.set_yticklabels([f'2^{i}' for i in range(4,9)])
ax.set_yscale('log', base=2)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=8)

# Display the plot
plt.tight_layout()
plt.show()


# Plot Path Length
path_data = rearrange_data(data, 'path_length')
# Creating a bar plot for Path Length with standard deviation
fig, ax = plt.subplots(figsize=(24, 8))

# Test levels and corresponding data
levels = list(path_data.keys())
nodes = sorted(list(path_data[levels[0]].keys()))

group_width = bar_width * len(levels)  # Total width of all bars in a group

# Plotting each distrib separately
for i, distrib in enumerate(distribs):
    for j, level in enumerate(levels):
        avg_values = [path_data[level][node][distrib]['average'] for node in nodes]
        std_dev_values = [path_data[level][node][distrib]['std_dev'] for node in nodes]

        # Plotting the bars with standard deviation as error bars
        x = [pos + (i * len(levels) + j) * bar_width for pos in range(len(nodes))]
        color = color_palettes[distrib][j]
        # slightly modify the color for better visibility
        coloe = (color[0], color[1], color[2], 0.9)
        bars = ax.bar(x, avg_values, width=bar_width, label=f"{distrib} {level}", color=coloe)
        # plot error bars
        ax.errorbar(x, avg_values, yerr=std_dev_values, fmt='none', ecolor=color, capsize=5, capthick=2)

# Adding labels
ax.set_xlabel('Number of Nodes')
ax.set_ylabel('Path Length')
ax.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax.set_xticklabels(nodes)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=8)

# Display the plot

plt.tight_layout()

plt.show()

# miss percentage
miss_data = rearrange_data(data, 'misses')

# Creating a bar plot for Miss Percentage
fig, ax = plt.subplots(figsize=(24, 8))

# Test levels and corresponding data
levels = list(miss_data.keys())
nodes = sorted(list(miss_data[levels[0]].keys()))

group_width = bar_width * len(levels)  # Total width of all bars in a group

# Plotting each distrib separately
for i, distrib in enumerate(distribs):
    reps = 1 if distribution in ["sobol_unscr", "halton_unscr", "mpmc"] else args.reps
    for j, level in enumerate(levels):
        values = [100*miss_data[level][node][distrib]/(reps*40) for node in nodes]

        # Plotting the bars
        x = [pos + (i * len(levels) + j) * bar_width for pos in range(len(nodes))]
        color = color_palettes[distrib][j]
        color = (color[0], color[1], color[2], 0.9)

        ax.bar(x, values, width=bar_width, label=f"{distrib} {level}", color=color)

# Adding labels
ax.set_xlabel('Number of Nodes')
ax.set_ylabel('Miss Percentage (%)')
ax.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax.set_xticklabels(nodes)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=8)

# Display the plot
plt.tight_layout()
plt.show()

# Gain
gain_data = rearrange_data(data, 'percentage_gain')

# Creating a bar plot for Gain with a log base 2 scale for the y-axis
# Test levels and corresponding data
levels = list(gain_data.keys())
nodes = sorted(list(gain_data[levels[0]].keys()))

# Create the figure and two subplots with a broken y-axis
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,
                               figsize=(24, 8),        # Set the figure size to 12x8 inches
                               gridspec_kw={'height_ratios': [3, 1]})

# Plotting each distrib separately in both subplots
group_width = (bar_width * (len(distribs)-1)* len(levels))

# distribs minus uniform
deestribs = ['sobol_scram', 'sobol_unscr', 'mpmc', 'halton_unscr', 'halton_scram', 'tri_lat', 'sukharev']

for i, distrib in enumerate(deestribs):
        for j, level in enumerate(levels):
            values = [gain_data[level][node][distrib] for node in nodes]
            # Plotting the bars
            x = [pos + (i * len(levels) + j) * bar_width for pos in range(len(nodes))]
            color = color_palettes[distrib][j]
            color = (color[0], color[1], color[2], 0.9)

            ax1.bar(x, values, width=bar_width, label=f"{distrib} {level}", color=color)
            ax2.bar(x, values, width=bar_width, color=color)

# Adjust y-limits for each subplot
ax1.set_ylim(-2, 16)  # Upper range for the main plot
ax2.set_ylim(-20, -26)  # Lower range for the zoomed-in negative values

# Hide the spines and ticks where the break occurs
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # Don't put tick labels at the top
ax2.xaxis.tick_bottom()

# Add parallel diagonal lines to indicate the break
d = .015  # Size of the diagonal lines in axes coordinates
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)

# Draw diagonal lines for the upper subplot
ax1.plot((-d, +d), (-d, +d), **kwargs)        # Top-left diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # Top-right diagonal

# Switch to the bottom axes
kwargs.update(transform=ax2.transAxes)

# Draw diagonal lines for the lower subplot (at the top of ax2)
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # Top-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # Top-right diagonal


# Adding labels
ax2.set_xlabel('Number of Nodes')
ax1.set_ylabel('Gain (%)')
ax2.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax2.set_xticklabels(nodes)
# flip ax2 y axis
ax2.invert_yaxis()
# make legend above the plot, horizontally
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=7)
# make ticks on y multiples of 5
ax1.set_yticks(range(0, 16, 5))
ax2.set_yticks(range(-20, -26, -5))

# Display the plot
plt.tight_layout()
plt.show()

