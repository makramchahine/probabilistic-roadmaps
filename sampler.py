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

    # Check if n_points is valid
    ns_allowed = [32, 64, 128, 256, 512, 1024]
    assert n_points in ns_allowed, f"n_points must be one of {ns_allowed}"

    # Check if dist is valid
    dists_allowed = ["uniform", "sobol_scram", "sobol_unscr", "mpmc"]
    assert dist in dists_allowed, f"dist must be one of {dists_allowed}"

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

    return x