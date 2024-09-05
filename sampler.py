# this function samples 2D points on the unit square according to the input distribution and number of points
# distributions include: uniform, sobol, and custom mpmc

import numpy as np
import torch
import matplotlib.pyplot as plt
from scipy.stats.qmc import discrepancy as L2discrepancy
from scipy.stats import qmc
import os

def get_best_batch_id(data, nsamples):
    nb = int(data.shape[0] / nsamples)
    discs = []
    for batch_id in range(nb):
        x = data[batch_id * nsamples:(batch_id + 1) * nsamples]
        discs.append(L2discrepancy(x,method='L2-star'))
    discs = np.array(discs)
    arg = np.argmin(discs)

    return arg, discs[arg]

def sampler(n_points = 32, dist = "uniform", rep=0):
    if dist in ["mpmc", "mpmc_rand", "mpmc_batch", "mpmc_l2bat"]:
        # Check if n_points is valid
        ns_allowed = [32, 64, 128, 256, 512, 1024]
        assert n_points in ns_allowed, f"n_points must be one of {ns_allowed} for {dist} distribution"

    if dist == "uniform":
        x = np.random.rand(n_points, 2)

    elif dist == "sobol_scram":
        x = qmc.Sobol(2, scramble=True).random(n_points)

    elif dist == "sobol_unscr":
        x = qmc.Sobol(2, scramble=False).random(n_points)

    elif dist == "sobol_batch":
        sobol_sampler = qmc.Sobol(2, scramble=False)
        sobol_sampler.fast_forward(rep*n_points + 1)
        x = sobol_sampler.random(n_points)


    elif dist == "sobol_rand":
        x = qmc.Sobol(2, scramble=False).random(n_points)
        x += np.random.rand(2)
        x = x % 1

    elif dist == "mpmc":
        path = "/home/makramchahine/repos/PRM/MPMC_points/MPMC_d2_N"+str(n_points)+".npy"
        data = np.load(path)
        b_id, _ = get_best_batch_id(data, n_points)
        x = data[b_id * n_points:(b_id + 1) * n_points]

    elif dist == "mpmc_batch":
        path = "/home/makramchahine/repos/PRM/MPMC_points/MPMC_d2_N"+str(n_points)+".npy"
        data = np.load(path)
        bs = int(data.shape[0]/n_points)
        if rep >= bs:
            return None
        else:
            x = data[rep * n_points:(rep + 1) * n_points]

    elif dist == "mpmc_l2bat":
        path = "/home/makramchahine/repos/PRM/L2_MPMC_points/MPMC_d2_N"+str(n_points)+".npy"
        data = np.load(path)
        bs = int(data.shape[0]/n_points)
        if rep >= bs:
            return None
        else:
            x = data[rep * n_points:(rep + 1) * n_points]

    elif dist == "mpmc_rand":
        path = "/home/makramchahine/repos/PRM/MPMC_points/MPMC_d2_N"+str(n_points)+".npy"
        data = np.load(path)
        b_id, _ = get_best_batch_id(data, n_points)
        x = data[b_id * n_points:(b_id + 1) * n_points]

        # add a random translation to the points
        x += np.random.rand(2)
        # make sure the points are still in the unit square (mod 1)
        x = x % 1

    elif dist == "mpmc_seq":
        path = "/home/makramchahine/repos/PRM/MPMC_points/ordered_MPMC_d2_N1024.npy"
        data = np.load(path)
        x = data[:n_points]

    elif dist == "halton_scram":
        x = qmc.Halton(2, scramble=True).random(n_points)

    elif dist =="halton_unscr":
        x = qmc.Halton(2, scramble=False).random(n_points)

    elif dist =="halton_batch":
        halton_sampler = qmc.Halton(d=2,scramble=False)
        halton_sampler.fast_forward(rep*n_points)
        x = halton_sampler.random(n_points)
    
    elif dist =="halton_rand":
        x = qmc.Halton(2, scramble=False).random(n_points)
        # add a random translation to the points
        x += np.random.rand(2)
        # make sure the points are still in the unit square (mod 1)
        x = x % 1

    elif dist =="tri_lat":
        # find the smallest square grid that can fit n_points
        n_side = int(np.ceil(np.sqrt(n_points)))
        
        # Set y_spacing to span the full height with n_side points
        y_spacing = 1 / n_side
        
        # Calculate x_spacing to maintain the sqrt(3)/2 ratio
        x_spacing = y_spacing / (np.sqrt(3) / 2)
        
        # Generate grid of points
        x = []
        for i in range(n_side):
            for j in range(n_side):
                x_coord = i * x_spacing
                y_coord = j * y_spacing
                
                # Shift every other row by half the x_spacing
                if j % 2 == 1:
                    x_coord += 0.5 * x_spacing
                
                # Only include points within the unit square
                if x_coord <= 1 and y_coord <= 1:
                    x.append([x_coord, y_coord])
        
        # Convert to numpy array
        x = np.array(x)

        # shift all the values up by half the spacing at the top
        x[:,1] += (1 - max(x[:,1]))/2
        # shift all the values to the right by half the spacing at the right
        x[:,0] += (1 - max(x[:,0]))/2

        n_generated = len(x)
        
        # Remove random points until we have n_points
        while n_generated > n_points:
            # Randomly sample points from the points generated so far
            idx = np.random.choice(n_generated)
            x = np.delete(x, idx, axis=0)
            n_generated -= 1

        # rotate all point by 10*pi
        theta = 10 * np.pi / 180
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        x = np.dot(x, rot)
        # bring all points back to the unit square
        x = x % 1

    elif dist =="tri_lat_add":
        # Estimate the number of points along each direction
        n_side = int(np.floor(np.sqrt(n_points)))
        
        # Set y_spacing to span the full height with n_side points
        y_spacing = 1 / n_side
        
        # Calculate x_spacing to maintain the sqrt(3)/2 ratio
        x_spacing = y_spacing / (np.sqrt(3) / 2)
        
        # Generate grid of points
        x = []
        for i in range(n_side):
            for j in range(n_side):
                x_coord = i * x_spacing
                y_coord = j * y_spacing
                
                # Shift every other row by half the x_spacing
                if j % 2 == 1:
                    x_coord += 0.5 * x_spacing
                
                # Only include points within the unit square
                if x_coord <= 1 and y_coord <= 1:
                    x.append([x_coord, y_coord])
        
        # Convert to numpy array
        x = np.array(x)

        # shift all the values up by half the spacing at the top
        x[:,1] += (1 - max(x[:,1]))/2
        # shift all the values to the right by half the spacing at the right
        x[:,0] += (1 - max(x[:,0]))/2
        
        # Number of points generated so far
        n_generated = len(x)
        
        # Generate the remaining points by taking a random sample of the points generated so far and shifting them by yspacing/2 in the y direction
        while n_generated < n_points:
            # Randomly sample points from the points generated so far
            idx = np.random.choice(n_generated)
            # plus min
            pmy = np.random.choice([-1,1])
            # Shift the sampled point by sqrt(3)/4 in the y direction
            new_point = x[idx] + np.array([0, pmy * 2* y_spacing/3])
            # Only include the new point if it is within the unit square and not already in the list
            if new_point[0] <= 1 and new_point[1] <= 1 and new_point[0] >= 0 and new_point[1] >= 0:
                if not any(np.all(np.isclose(new_point, x), axis=1)):
                    x = np.vstack((x, new_point))
                    n_generated += 1
        
        # rotate all point by 10*pi
        theta = 10 * np.pi / 180
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        x = np.dot(x, rot)
        # bring all points back to the unit square
        x = x % 1

    elif dist == "sukharev_add":
        # make a grid of points
        n = int(np.sqrt(n_points))
        x = np.array([[i/n, j/n] for i in range(n) for j in range(n)])
        # shift by half the spacing in the x direction
        x[:,0] += 1/(2*n)
        # shift by half the spacing in the y direction
        x[:,1] += 1/(2*n)

        # add the remaining points by taking a random sample of the points generated so far and shifting them by yspacing/2 in the y direction
        while len(x) < n_points:
            idx = np.random.choice(len(x))
            pmx = np.random.choice([-1,1])
            pmy = np.random.choice([-1,1])
            new_point = x[idx] + np.array([pmx, pmy]) * 1/(2*n)
            if new_point[0] < 1 and new_point[1] < 1 and new_point[0] > 0 and new_point[1] > 0:
                if not any(np.all(np.isclose(new_point, x), axis=1)):
                    x = np.vstack((x, new_point))
        
        # rotate all point by 10*pi
        theta = 10 * np.pi / 180 
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        x = np.dot(x, rot)
        # bring all points back to the unit square
        x = x % 1

    elif dist == "sukharev":
        # find the smallest square grid that can fit n_points
        n = np.ceil(np.sqrt(n_points))
        # generate the grid
        x = np.array([[i/n, j/n] for i in range(int(n)) for j in range(int(n))])
        # shift by half the spacing in the x direction
        x[:,0] += 1/(2*n)
        # shift by half the spacing in the y direction
        x[:,1] += 1/(2*n)

        # remove random points until we have n_points
        while len(x) > n_points:
            idx = np.random.choice(len(x))
            x = np.delete(x, idx, axis=0)

        # rotate all point by 10*pi/180
        theta = 10 * np.pi /180
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        x = np.dot(x, rot)
        # bring all points back to the unit square
        x = x % 1

    else:
        raise ValueError(f"Invalid distribution: {dist}")
    
    return x


# # List of distributions and number of nodes
# # Directory to save the plots
# output_dir = "results"
# os.makedirs(output_dir, exist_ok=True)

# dists = ["uniform", "sobol_scram", "sobol_unscr", "sobol_rand", "halton_scram", "halton_unscr", "halton_rand", "tri_lat", "tri_lat_add", "sukharev", "sukharev_add", "mpmc", "mpmc_rand", "mpmc_seq"]
# nodes = [32, 64, 128, 256, 512, 1024]

# # # Initialize a dictionary to store the discrepancies
# disc = {dist: {node: [] for node in nodes} for dist in dists}

# # Compute the L2 discrepancy for each distribution and number of nodes
# for dist in dists:
#     for node in nodes:
#         for _ in range(10):
#             x = sampler(n_points=node, dist=dist)
#             disc[dist][node].append(L2discrepancy(x, method='L2-star'))

# # Compute the mean discrepancies
# mean_disc = {dist: {node: np.mean(disc[dist][node]) for node in nodes} for dist in dists}

# # Plot the bar plots
# for node in nodes:
#     means = [mean_disc[dist][node] for dist in dists]

#     plt.figure(figsize=(10, 6))
#     plt.bar(dists, means, color='skyblue')
#     plt.xlabel('Distributions')
#     plt.ylabel('Mean L2 Discrepancy')
#     plt.title(f'Mean L2 Discrepancy for {node} Nodes')
#     plt.xticks(rotation=45, ha='right')
#     plt.yscale('log')
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, f"mean_disc_{node}.png"))
#     plt.close()

# # plot the points sampled


# # Loop over each distribution type
# for dist in ["uniform", "sobol_scram", "sobol_unscr", "sobol_rand", "halton_scram", "halton_unscr", "halton_rand", "tri_lat", "tri_lat_add", "sukharev", "sukharev_add", "mpmc", "mpmc_rand", "mpmc_seq"]:
#     # Sample 64 points using the specified distribution
#     x = sampler(n_points=32, dist=dist)

#     # Create a scatter plot
#     plt.figure(figsize=(6, 6))
#     plt.scatter(x[:, 0], x[:, 1], color='blue', s=10)
#     plt.axis('equal')
#     plt.title(f'Sampled Points - {dist}')
#     plt.xlabel('X-axis')
#     plt.ylabel('Y-axis')

#     # Save the plot
#     plt.savefig(os.path.join(output_dir, f"{dist}.png"))
#     plt.close()  # Close the plot to avoid overlapping plots

# # run halton_unscr 10 times and plot the points on the subplots
# fig = plt.figure(figsize=(10, 10))
# for n in range(1,10):
#     plt.subplot(3, 3, n)
#     x = sampler(n_points=n+5, dist="sobol_unscr")
#     plt.scatter(x[:, 0], x[:, 1], s=10)
#     plt.axis('equal')
# plt.savefig("halton_unscr.png")

# plot halton_unscr, sobol_unscr with 16 and 32 points on two subplots (one per distribution)

# n1 = 256
# n2 = 128

# fig = plt.figure(figsize=(10, 5))
# plt.subplot(1, 2, 1)
# x = sampler(n_points=n1, dist="sobol_unscr")
# # in blue
# plt.scatter(x[:, 0], x[:, 1], s=10, color='blue', alpha=0.5)
# # now 32 in red 
# x = sampler(n_points=n2, dist="sobol_unscr")
# plt.scatter(x[:, 0], x[:, 1], s=10, color='gold', alpha=0.5)
# plt.axis('equal')
# plt.title("sobol_unscr")

# plt.subplot(1, 2, 2)
# x = sampler(n_points=n1, dist="halton_unscr")
# # in blue
# plt.scatter(x[:, 0], x[:, 1], s=10, color='blue', alpha=0.5)
# # now 32 in red
# x = sampler(n_points=n2, dist="halton_unscr")
# plt.scatter(x[:, 0], x[:, 1], s=10, color='gold', alpha=0.5)
# plt.axis('equal')
# plt.title("halton_unscr")
# plt.savefig("sobol_halton_unscr.png")

# # plot the mpmc_batch distribution with 32 points for over 32 reps
# for rep in range(32):
#     x = sampler(n_points=32, dist="mpmc_batch", rep=rep)
#     if x is not None:
#         plt.scatter(x[:, 0], x[:, 1], s=10)
# plt.axis('equal')
# plt.savefig("mpmc_batch.png")

# plot the halton_batch distribution with different rep seeds
for rep in range(3):
    x = sampler(n_points=16, dist="sobol_batch", rep=rep)
    plt.scatter(x[:, 0], x[:, 1], s=10)
plt.axis('equal')
plt.savefig("halton_batch.png")
