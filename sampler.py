# this function samples 2D points on the unit square according to the input distribution and number of points
# distributions include: uniform, sobol, and custom mpmc

import numpy as np
import torch
import matplotlib.pyplot as plt
from scipy.stats.qmc import discrepancy as L2discrepancy
from scipy.stats import qmc

def get_best_batch_id(data, nsamples):
    nb = int(data.shape[0] / nsamples)
    discs = []
    for batch_id in range(nb):
        x = data[batch_id * nsamples:(batch_id + 1) * nsamples]
        discs.append(L2discrepancy(x,method='L2-star'))
    discs = np.array(discs)
    arg = np.argmin(discs)

    return arg, discs[arg]

def sampler(n_points = 32, dist = "uniform"):

    # Check if dist is valid
    dists_allowed = ["uniform", "sobol_scram", "sobol_unscr", "halton_scram", "halton_unscr", "tri_lat", "sukharev", "mpmc"]
    assert dist in dists_allowed, f"dist must be one of {dists_allowed}"

    if not dist=="uniform":
        # Check if n_points is valid
        ns_allowed = [32, 64, 128, 256, 512, 1024]
        assert n_points in ns_allowed, f"n_points must be one of {ns_allowed} for {dist} distribution"

    if dist == "uniform":
        x = np.random.rand(n_points, 2)

    elif dist == "sobol_scram":
        x = qmc.Sobol(2, scramble=True).random(n_points)

    elif dist == "sobol_unscr":
        x = qmc.Sobol(2, scramble=False).random(n_points)

    elif dist == "mpmc":
        path = "/home/makramchahine/repos/PRM/MPMC_points/MPMC_d2_N"+str(n_points)+".npy"
        data = np.load(path)
        b_id, _ = get_best_batch_id(data, n_points)
        x = data[b_id * n_points:(b_id + 1) * n_points]

    elif dist == "halton_scram":
        x = qmc.Halton(2, scramble=True).random(n_points)

    elif dist =="halton_unscr":
        x = qmc.Halton(2).random(n_points)

    elif dist =="tri_lat":
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

    elif dist == "sukharev":
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
            if new_point[0] <= 1 and new_point[1] <= 1 and new_point[0] >= 0 and new_point[1] >= 0:
                if not any(np.all(np.isclose(new_point, x), axis=1)):
                    x = np.vstack((x, new_point))

    
    return x

# for each of the distributions, generate 32 points and plot them
dists = ["sukharev"]#, "sobol_scram", "sobol_unscr", "uniform", "mpmc", "halton_scram", "halton_unscr"]
for dist in dists:
    x = sampler(n_points=128, dist=dist)
    plt.scatter(x[:,0], x[:,1], label=dist)
plt.legend()
plt.axis('equal')
plt.xlim(0,1)
plt.ylim(0,1)
plt.savefig("results/sampler_comparison.png")