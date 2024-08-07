import pygame
import environment
import graph
import argparse
import sys
from sampler import sampler
import numpy as np
import matplotlib.pyplot as plt

# Command line arguments
parser = argparse.ArgumentParser(description='Implements the PRM algorithm for path planning.')
parser.add_argument('-o', '--obstacles', type=bool, action=argparse.BooleanOptionalAction,
                    metavar='', required=False, help='Obstacles on the map')
parser.add_argument('-i', '--iterations', type=int, metavar='', required=False, default=10,
                    help='Number of iterations to run')
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
args = parser.parse_args()

# Initialization
pygame.init()

# Constants
MAP_DIMENSIONS = 640, 480

def random_init_goal_positions():
    x_init = (np.random.randint(0, MAP_DIMENSIONS[0]), np.random.randint(0, MAP_DIMENSIONS[1] // 4))
    x_goal = (np.random.randint(0, MAP_DIMENSIONS[0]), np.random.randint(3 * MAP_DIMENSIONS[1] // 4, MAP_DIMENSIONS[1]))
    return x_init, x_goal

def run_prm_iteration(distribution, x_init, x_goal):
    environment_ = environment.Environment(map_dimensions=MAP_DIMENSIONS)
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
        #     graph_.draw_roadmap(configurations=success_configurations, nears=success_nears, map_=environment_.map, k=k)
        #     graph_.draw_trajectory(configurations=success_configurations, nears=success_nears, environment=environment_,
        #                            obstacles=obstacles, k=k, keep_roadmap=args.keep_roadmap)
        #     graph_.draw_path_to_goal(map_=environment_.map, environment=environment_, obstacles=obstacles)
            break

        # pygame.display.update()

    return path_length, graph_.path_coordinates


def main():
    samplers = ['sobol_scram', 'sobol_unscr', 'uniform', 'mcmp']
    results = {sampler: {'lengths': [], 'paths': [], 'init_goal_positions': []} for sampler in samplers}

    iterations = args.iterations

    for iteration in range(iterations):
        x_init, x_goal = random_init_goal_positions()
        ok = False
        while not ok:
            try:
                run_prm_iteration('uniform', x_init, x_goal)
                ok = True
            except:
                x_init, x_goal = random_init_goal_positions()
        for distribution in samplers:
            iterations = 10 if distribution in ['sobol_scram', 'uniform'] else 1
            for _ in range(iterations):
                ok = False
                while not ok:
                    try:
                        path_length, path_coordinates = run_prm_iteration(distribution, x_init, x_goal)
                        ok = True
                    except:
                        path_length, path_coordinates = run_prm_iteration(distribution, x_init, x_goal)
                print(f'{distribution} at iteration {iteration}: {path_length}')
                if path_length:
                    results[distribution]['lengths'].append(path_length)
                    results[distribution]['paths'].append(path_coordinates)
                    results[distribution]['init_goal_positions'].append((x_init, x_goal))

    # Plotting results
    plt.figure()
    colors = {'sobol_scram': 'r', 'sobol_unscr': 'orange', 'uniform': 'm', 'mcmp': 'g'}

    for distribution, data in results.items():
        for path_coordinates in data['paths']:
            xs, ys = zip(*path_coordinates)
            plt.plot(xs, ys, color=colors[distribution], label=f'{distribution} path', alpha=0.5)

    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('PRM Paths for Different Samplers')
    plt.gca().invert_yaxis()  # Flip y-axis to match pygame
    plt.gca().set_aspect('equal', adjustable='box')  # Ensure axes aspect ratio is equal
    # add unique id to the saved name
    name = 'results/all_paths_'+str(args.nodes)+"_"+str(args.iterations)+'.png'
    plt.savefig(name)
    plt.show()

    # Print results
    for distribution, data in results.items():
        print(f'Sampler: {distribution}')
        print(f'  Average Path Length: {np.mean(data["lengths"])}')
        print(f'  Std Dev Path Length: {np.std(data["lengths"])}')

    # save the results to a numpy file
    np.save('results/results_'+str(args.nodes)+"_"+str(args.iterations)+'.npy', results)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
