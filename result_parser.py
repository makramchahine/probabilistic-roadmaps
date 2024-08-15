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
                    sobol_scram = float(row[1])
                    sobol_unscr = float(row[2])
                    uniform = float(row[3])
                    mpmc = float(row[4])

                    # Store data
                    data[level][points][metric] = {
                        'sobol_scram': sobol_scram,
                        'sobol_unscr': sobol_unscr,
                        'uniform': uniform,
                        'mpmc': mpmc
                    }

    return data


# Example usage
directory = "/home/makramchahine/repos/PRM/results/analysis"
data = parse_csv_files(directory)

# Rearrange data structure
cardinality_data = defaultdict(lambda: defaultdict(dict))
for level, points_data in data.items():
    for points, metrics in points_data.items():
        cardinality_data[f'level_{level}'][points] = {
            'sobol_scram': {
                'average': metrics['average_cardinality']['sobol_scram'],
                'std_dev': metrics['std_dev_cardinality']['sobol_scram']
            },
            'sobol_unscr': {
                'average': metrics['average_cardinality']['sobol_unscr'],
                'std_dev': metrics['std_dev_cardinality']['sobol_unscr']
            },
            'uniform': {
                'average': metrics['average_cardinality']['uniform'],
                'std_dev': metrics['std_dev_cardinality']['uniform']
            },
            'mpmc': {
                'average': metrics['average_cardinality']['mpmc'],
                'std_dev': metrics['std_dev_cardinality']['mpmc']
            }
        }

# Creating a bar plot for Cardinality with standard deviation, with a log base 2 scale for the y-axis
fig, ax = plt.subplots(figsize=(12, 8))

# Test conditions and corresponding data
conditions = list(cardinality_data.keys())
nodes = sorted(list(cardinality_data[conditions[0]].keys()))
methods = ['sobol_scram', 'sobol_unscr', 'uniform', 'mpmc']

bar_width = 0.05  # Width of the bars
group_width = bar_width * len(conditions)  # Total width of all bars in a group

# Define color palettes for each method
greens = plt.cm.Greens(np.linspace(0.3, 0.8, len(conditions)))
blues = plt.cm.Blues(np.linspace(0.3, 0.8, len(conditions)))
oranges = plt.cm.Oranges(np.linspace(0.3, 0.8, len(conditions)))
purples = plt.cm.Purples(np.linspace(0.3, 0.8, len(conditions)))

color_palettes = {
    'mpmc': greens,
    'sobol_scram': blues,
    'sobol_unscr': purples,
    'uniform': oranges
}

# Plotting each method separately
for i, method in enumerate(methods):
    for j, condition in enumerate(conditions):
        avg_values = [cardinality_data[condition][node][method]['average'] for node in nodes]
        std_dev_values = [cardinality_data[condition][node][method]['std_dev'] for node in nodes]

        # Plotting the bars with standard deviation as error bars
        x = [pos + (i * len(conditions) + j) * bar_width for pos in range(len(nodes))]
        color = color_palettes[method][j]
        ax.bar(x, avg_values, yerr=std_dev_values, width=bar_width, label=f"{method} {condition}", color=color)

# Adding labels and title
ax.set_xlabel('Number of Nodes')
ax.set_ylabel('Cardinality (log2 scale)')
ax.set_title('Cardinality Across Sampling Methods and Levels with Standard Deviation (log2 scale)')
ax.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax.set_xticklabels(nodes)
ax.set_yticks([2**i for i in range(4,9)])
ax.set_yticklabels([f'2^{i}' for i in range(4,9)])
ax.set_yscale('log', base=2)
ax.legend()

# Display the plot
plt.tight_layout()
plt.show()


# Rearrange data structure
path_data = defaultdict(lambda: defaultdict(dict))
for level, points_data in data.items():
    for points, metrics in points_data.items():
        path_data[f'level_{level}'][points] = {
            'sobol_scram': {
                'average': metrics['average_path_length']['sobol_scram'],
                'std_dev': metrics['std_dev_path_length']['sobol_scram']
            },
            'sobol_unscr': {
                'average': metrics['average_path_length']['sobol_unscr'],
                'std_dev': metrics['std_dev_path_length']['sobol_unscr']
            },
            'uniform': {
                'average': metrics['average_path_length']['uniform'],
                'std_dev': metrics['std_dev_path_length']['uniform']
            },
            'mpmc': {
                'average': metrics['average_path_length']['mpmc'],
                'std_dev': metrics['std_dev_path_length']['mpmc']
            }
        }

# Creating a bar plot for Path Length with standard deviation, with a log base 2 scale for the y-axis
fig, ax = plt.subplots(figsize=(12, 8))

# Test conditions and corresponding data
conditions = list(path_data.keys())
print(conditions)
nodes = sorted(list(path_data[conditions[0]].keys()))
methods = ['sobol_scram', 'sobol_unscr', 'uniform', 'mpmc']

group_width = bar_width * len(conditions)  # Total width of all bars in a group

# Define color palettes for each method
greens = plt.cm.Greens(np.linspace(0.3, 0.8, len(conditions)))
blues = plt.cm.Blues(np.linspace(0.3, 0.8, len(conditions)))
oranges = plt.cm.Oranges(np.linspace(0.3, 0.8, len(conditions)))
purples = plt.cm.Purples(np.linspace(0.3, 0.8, len(conditions)))

color_palettes = {
    'mpmc': greens,
    'sobol_scram': blues,
    'sobol_unscr': purples,
    'uniform': oranges
}

# Plotting each method separately
for i, method in enumerate(methods):
    for j, condition in enumerate(conditions):
        avg_values = [path_data[condition][node][method]['average'] for node in nodes]
        std_dev_values = [path_data[condition][node][method]['std_dev'] for node in nodes]

        # Plotting the bars with standard deviation as error bars
        x = [pos + (i * len(conditions) + j) * bar_width for pos in range(len(nodes))]
        color = color_palettes[method][j]
        # slightly modify the color for better visibility
        coloe = (color[0], color[1], color[2], 0.9)
        bars = ax.bar(x, avg_values, width=bar_width, label=f"{method} {condition}", color=coloe)
        # plot error bars
        ax.errorbar(x, avg_values, yerr=std_dev_values, fmt='none', ecolor=color, capsize=5, capthick=2)

# Adding labels and title
ax.set_xlabel('Number of Nodes')
ax.set_ylabel('Path Length')
# # y scale log
ax.set_yscale('log', base=10)
# ax.set_title('Path Length Across Sampling Methods and Levels with Standard Deviation')
ax.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax.set_xticklabels(nodes)
ax.legend()

# Display the plot

plt.tight_layout()

plt.show()


# Rearrange data structure
gain_data = defaultdict(lambda: defaultdict(dict))
for level, points_data in data.items():
    for points, metrics in points_data.items():
        gain_data[f'level_{level}'][points] = {
            'sobol_scram': metrics['percentage_gain']['sobol_scram'],
            'sobol_unscr': metrics['percentage_gain']['sobol_unscr'],
            'uniform': metrics['percentage_gain']['uniform'],
            'mpmc': metrics['percentage_gain']['mpmc']
        }

# Creating a bar plot for Gain with a log base 2 scale for the y-axis
# fig, ax = plt.subplots(figsize=(12, 8))

# Test conditions and corresponding data
conditions = list(gain_data.keys())
nodes = sorted(list(gain_data[conditions[0]].keys()))
methods = ['sobol_scram', 'sobol_unscr', 'mpmc']

group_width = bar_width * len(conditions)  # Total width of all bars in a group

# Define color palettes for each method
greens = plt.cm.Greens(np.linspace(0.3, 0.8, len(conditions)))
blues = plt.cm.Blues(np.linspace(0.3, 0.8, len(conditions)))
oranges = plt.cm.Oranges(np.linspace(0.3, 0.8, len(conditions)))
purples = plt.cm.Purples(np.linspace(0.3, 0.8, len(conditions)))

color_palettes = {
    'mpmc': greens,
    'sobol_scram': blues,
    'sobol_unscr': purples,
    'uniform': oranges
}
#
# # Plotting each method separately
# for i, method in enumerate(methods):
#     for j, condition in enumerate(conditions):
#         values = [gain_data[condition][node][method] for node in nodes]
#
#         # Plotting the bars
#         x = [pos + (i * len(conditions) + j) * bar_width for pos in range(len(nodes))]
#         color = color_palettes[method][j]
#         # slightly modify the color for better visibility
#         coloe = (color[0], color[1], color[2], 0.9)
#         bars = ax.bar(x, values, width=bar_width, label=f"{method} {condition}", color=coloe)
#
# # Adding labels and title
# ax.set_xlabel('Number of Nodes')
# ax.set_ylabel('Gain (%)')
# ax.set_title('Gain Against Uniform Across Sampling Methods and Levels')
# ax.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
# ax.set_xticklabels(nodes)
# ax.legend()


# Display the plot
plt.tight_layout()
bar_width = 0.07

# Create the figure and two subplots with a broken y-axis
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# Plotting each method separately in both subplots
group_width = bar_width * len(methods) * len(conditions)

for i, method in enumerate(methods):
    for j, condition in enumerate(conditions):
        values = [gain_data[condition][node][method] for node in nodes]

        # Plotting the bars
        x = [pos + (i * len(conditions) + j) * bar_width for pos in range(len(nodes))]
        color = color_palettes[method][j]
        color = (color[0], color[1], color[2], 0.9)

        ax1.bar(x, values, width=bar_width, label=f"{method} {condition}", color=color)
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


# Adding labels and title
ax2.set_xlabel('Number of Nodes')
ax1.set_ylabel('Gain (%)')
ax2.set_xticks([pos + group_width / 2 for pos in range(len(nodes))])
ax2.set_xticklabels(nodes)
# flip ax2 y axis
ax2.invert_yaxis()
# make legend above the plot, horizontally
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
# make ticks on y multiples of 5
ax1.set_yticks(range(0, 16, 5))
ax2.set_yticks(range(-20, -26, -5))

# Display the plot
plt.tight_layout()
plt.show()

plt.show()
