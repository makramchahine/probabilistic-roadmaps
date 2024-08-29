import pygame
import environment
import graph
import argparse
import sys
from sampler import sampler
import numpy as np
from tqdm import tqdm
import os

from config import SAMPLERS, MAP_DIMENSIONS, INITIAL

# Command line arguments
parser = argparse.ArgumentParser(description='Implements the PRM algorithm for path planning.')
parser.add_argument('-o', '--obstacles', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, help='Obstacles on the map')
parser.add_argument('-srn', '--show_random_nodes', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, help='Show random nodes on screen')
parser.add_argument('-n', '--nodes', type=int, metavar='', required=False, default=32,
                    help='Number of nodes to put in the roadmap')
parser.add_argument('-k', '--k_nearest', type=int, metavar='', required=False,
                    help='Number of the closest neighbors to examine for each configuration')
parser.add_argument('-kr', '--keep_roadmap', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, help='Keeps the tree while the robot is moving towards the goal')
parser.add_argument('-r', '--radius', type=int, metavar='', required=False, default=10,
                    help='Set the robot radius')
parser.add_argument('-s', '--save', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, default=False, help='Save the results to a numpy file')
parser.add_argument('--draw', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, default=False, help='Draw the environment')
parser.add_argument('--overwrite', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, default=True, help='Overwrite the results file')
parser.add_argument('-d', '--duration', type=float, default=0.02, help='Duration of the simulation')
parser.add_argument('--level', type=int, default=1, help='Difficulty level of the environment')
parser.add_argument('--reps', type=int, default=20, help='Number of repetitions for each randomized sampler')

args = parser.parse_args()

# Initialization
pygame.init()

def run_prm_iteration(distribution, x_init, x_goal, level):
    environment_ = environment.Environment(map_dimensions=MAP_DIMENSIONS, level=level)
    graph_ = graph.Graph(start=x_init, goal=x_goal, map_dimensions=MAP_DIMENSIONS, radius=args.radius)
    configurations = []
    nears = []
    success_configurations = []
    success_nears = []
    initial = graph_.draw_initial_node(map_=environment_.map)
    goal = graph_.draw_goal_node(map_=environment_.map)
    configurations.append(initial)
    configurations.append(goal)
    environment_.make_obstacles()
    obstacles = environment_.draw_obstacles() if args.obstacles else []
    graph_.obstacles = obstacles
    is_simulation_finished = False
    is_configuration_free = True

    # Number of nodes to put in the roadmap
    n = 0

    # Number of the closest neighbors to examine for each configuration
    k = args.k_nearest if args.k_nearest is not None else 15
    sampling = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        points = sampler(n_points=args.nodes, dist=distribution)

        if sampling:
            for point in points:
                x = graph_.generate_input_nodes(point)
                collision_free = graph_.is_free(point=x, obstacles=obstacles)
                if collision_free:
                    if args.show_random_nodes:
                        graph_.draw_random_node(map_=environment_.map)
                    configurations.append(x)
            sampling = False
            cardinality = len(configurations)

        if not sampling and not is_simulation_finished:
            for configuration in configurations:
                new_configurations = configurations.copy()
                new_configurations.remove(configuration)
                near = graph_.k_nearest(graph=new_configurations, x_rand=configuration, configuration=configuration,
                                        k=k)

                for i in range(k):
                    cross_obstacle = graph_.cross_obstacle(configuration1=configuration, configuration2=near[i],
                                                           map_=environment_.map)
                    if not cross_obstacle:
                        graph_.draw_local_planner(p1=configuration, p2=near[i], map_=environment_.map)
                        nears.append(near[i])
                        if is_configuration_free:
                            success_configurations.append(configuration)
                            is_configuration_free = False

                if nears != []:
                    success_nears.append(nears)
                    nears = []
                is_configuration_free = True

            graph_.a_star(nodes=configurations, map_=environment_.map)

            # Calculate path length
            path_length = 0
            for i in range(len(graph_.path_coordinates) - 1):
                path_length += np.linalg.norm(
                    np.array(graph_.path_coordinates[i]) - np.array(graph_.path_coordinates[i + 1]))

            is_simulation_finished = True

        if is_simulation_finished:
            if args.draw:
                graph_.draw_roadmap(configurations=success_configurations, nears=success_nears, map_=environment_.map, k=k)
                graph_.draw_trajectory(configurations=success_configurations, nears=success_nears, environment=environment_,
                                       obstacles=obstacles, k=k, keep_roadmap=True, duration=args.duration)
                graph_.draw_path_to_goal(map_=environment_.map, environment=environment_, obstacles=obstacles)
            break

        pygame.display.update()

    return path_length, graph_.path_coordinates, cardinality


def main(samplers):
    results = {sampler: {'lengths': [], 'paths': [], 'init_goal_positions': [], 'cardinality': []} for sampler in samplers}

    level = args.level

    x_init, x_goal = [INITIAL[level]['start']], [INITIAL[level]['goal']]


    for i in tqdm(range(len(x_init))):
        for distribution in samplers:

            assert distribution in SAMPLERS, f'{distribution} is not a valid sampler'

            reps = 1 if distribution in ["sobol_unscr", "halton_unscr", "mpmc"] else args.reps
            for rep in tqdm(range(reps)):
                path_length, path_coordinates, cardinality = run_prm_iteration(distribution, x_init[i], x_goal[i], level)
                if not path_coordinates:
                    continue
                    # print(f'Miss {distribution} at rep {rep} and cardinality {cardinality}')
                else:
                    results[distribution]['lengths'].append(path_length)
                    results[distribution]['paths'].append(path_coordinates)
                    results[distribution]['init_goal_positions'].append((x_init, x_goal))
                    results[distribution]['cardinality'].append(cardinality)

    if args.save:
        file = "results/results_" + str(args.nodes) + "_" + str(args.reps) + "_" + str(args.level) + ".npy"
        print(f'This is {args.nodes} nodes and {args.reps} reps at level {args.level}')
        exists = os.path.exists(file)

        if exists:
            old_results = np.load(file, allow_pickle=True).item()

            # keys that are in results but not in old_results
            new_keys = [key for key in results.keys() if key not in old_results.keys()]

            # keys that are in both results and old_results
            common_keys = [key for key in results.keys() if key in old_results.keys()]
            
            for key in new_keys:
                # add the key to the old results
                old_results[key] = results[key]
                print(f'{key} results added')
            if args.overwrite:
                # overwrite the key in the old results
                for key in common_keys:
                    old_results[key] = results[key]
                    print(f'{key} results overwritten')
            np.save(file, old_results)
        else:
            np.save(file, results)
            print(f'Results saved to {file}')

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    # samplers = ["uniform", "sobol_scram", "sobol_unscr", "halton_scram", "halton_unscr", "tri_lat", "tri_lat_add", "sukharev", "sukharev_add", "mpmc", "mpmc_rand"]
    # samplers = ["uniform", "sobol_scram", "halton_scram", "tri_lat", "sukharev"]# "mpmc_rand"]
    samplers = ["sobol_rand", "halton_rand"]
    main(samplers)
