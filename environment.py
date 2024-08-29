import pygame
import os
import numpy as np

from config import MAP_DIMENSIONS, POSI, INIT

class Environment:
    '''
    A class of the map where the robot will be moving around.

    Attributes
    ----------
    dimensions : tuple
        The X and Y window dimensions.
    '''
    
    def __init__(self, map_dimensions, level = (1,)):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BROWN = (189, 154, 122)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.GRAY = (105, 105, 105)
        (self.WIDTH, self.HEIGHT) = map_dimensions
        self.FPS = 120
        pygame.display.set_caption('PRM')
        self.map = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.map.fill(self.WHITE)
        self.level = level
        self.obstacles = []

    
    def make_obstacles_T(self, initial_point, width, height = (50, 150)):
        '''
        Given a initial point, it makes a obstacle with shape of T.
        
        Parameters
        ----------
        initial_point : tuple
            X and Y coordinates, starting from the top-left most part where
            the obstacle will be placed.
        
        Returns
        -------
        list
            A collection of sides composing the T obstacle.        
        '''
        x = initial_point[0]
        y = initial_point[1]
        side1 = pygame.Rect(x, y, height, width)
        side2 = pygame.Rect(x + height // 2 - width // 2, y, width, height)
        obstacle = [
            side1,
            side2]
        return obstacle

    
    def make_obstacles_L(self, initial_point, width, height = (50, 150)):
        '''
        Given a initial point, it makes a obstacle with shape of L.
        
        Parameters
        ----------
        initial_point : tuple
            X and Y coordinates, starting from the top-left most part where
            the obstacle will be placed.
        
        Returns
        -------
        list
            A collection of sides composing the L obstacle.
        '''
        x = initial_point[0]
        y = initial_point[1]
        side1 = pygame.Rect(x, y, width, height)
        side2 = pygame.Rect(x, y + height - width, height, width)
        obstacle = [
            side1,
            side2]
        return obstacle

    
    def make_obstacles_I(self, initial_point, width, height = (50, 150)):
        '''
        Given a initial point, it makes a obstacle with shape of I.

        Parameters
        ----------
        initial_point : tuple
            X and Y coordinates, starting from the top-left most part where
            the obstacle will be placed.

        Returns
        -------
        list
            A collection of sides composing the I obstacle.
        '''
        x = initial_point[0]
        y = initial_point[1]
        side1 = pygame.Rect(x, y, width, height)
        obstacle = [
            side1]
        return obstacle

    
    def make_obstacles_M(self, initial_point, width, height = (150, 150)):
        '''
        Given a initial point, it makes a obstacle with shape of M.

        Parameters
        ----------
        initial_point : tuple
            X and Y coordinates, starting from the top-left most part where
            the obstacle will be placed.

        Returns
        -------
        list
            A collection of sides composing the M obstacle.
        '''
        x = initial_point[0]
        y = initial_point[1]
        side1 = pygame.Rect(x, y, width // 4, height)
        side2 = pygame.Rect(x + width // 2 - width // 12, y, width // 4, height)
        side3 = pygame.Rect(x + width - width // 6, y, width // 4, height)
        side4 = pygame.Rect(x + width // 6, y, width - width // 3, height // 4)
        obstacle = [
            side1,
            side2,
            side3,
            side4]
        return obstacle

    
    def make_obstacle_C(self, initial_point, width, height = (50, 150)):
        '''
        Given an initial point, it makes an obstacle with the shape of a "C".

        Parameters
        ----------
        initial_point : tuple
            X and Y coordinates, starting from the top-left most part where
            the obstacle will be placed.
        width : int, optional
            The width of the "C" shape, default is 50.
        height : int, optional
            The height of the "C" shape, default is 150.

        Returns
        -------
        list
            A collection of sides composing the "C" obstacle as pygame.Rect objects.
        '''
        (x, y) = initial_point
        thickness = max(1, height // 3)
        side1 = pygame.Rect(x, y, thickness, height)
        side2 = pygame.Rect(x, y, width, thickness)
        side3 = pygame.Rect(x, y + height - thickness, width, thickness)
        obstacle = [
            side1,
            side2,
            side3]
        return obstacle

    
    def generate_maze_I(self):
        """
        Generate a maze-like environment with 'I' shaped obstacles restricted to the middle 2/3rds of the map vertically.
        """
        maze_obstacles = []
        spacing = 10
        obstacle_width = 60
        obstacle_height = 60
        decal = 5
        decaf = 20
        y_min = self.HEIGHT // 6
        y_max = 5 * self.HEIGHT // 6
        for i in range(40):
            x = POSI[i + decal][0]
            y = POSI[i + decal][1]
            obstacle = self.make_obstacles_I((x, y), INIT[i + decaf][0], INIT[i + decaf][1])
            maze_obstacles.append(obstacle)
        self.obstacles = maze_obstacles

    
    def generate_inter_maze(self):
        maze_obstacles = []
        h_f = self.HEIGHT // 5
        w_f = self.WIDTH // 8
        wall_1 = self.make_obstacles_I((1 * w_f, 0), 20, 4 * h_f)
        maze_obstacles.append(wall_1)
        wall_2 = self.make_obstacles_I((2 * w_f , h_f), 20, 4 * h_f)
        maze_obstacles.append(wall_2)
        wall_3 = self.make_obstacles_I((3 * w_f , 0), 20, 2 * h_f)
        maze_obstacles.append(wall_3)
        wall_4 = self.make_obstacles_I((3 * w_f , 3 * h_f), 20, 2 * h_f)
        maze_obstacles.append(wall_4)

        rands = np.array([
            [0.544527, 0.144422],
            [0.985639, 0.9114],
            [0.561204, 0.896343],
            [0.252047, 0.453282],
            [0.82628, 0.520274],
            [0.314578, 0.168432],
            [0.754123, 0.0743171],
            [0.941966, 0.449393],
            [0.915798, 0.278299],
            [0.127793, 0.208063]])
        for i in range(10):
            x = int((3.75 + rands[i][0]) * w_f)
            y = int(rands[i][1] * self.HEIGHT)
            obstacle = self.make_obstacles_I((x, y), 30, 30)
            maze_obstacles.append(obstacle)

        # make a c shape obstacle
        obstacle = self.make_obstacle_C((6 * w_f, 1.5 * h_f), 1.5 * w_f, 1.85 * h_f)
        maze_obstacles.append(obstacle)

        self.obstacles = maze_obstacles


    
    def generate_complex_maze(self):
        maze_obstacles = []
        h_f = self.HEIGHT // 5
        w_f = self.WIDTH // 8
        for i in range(1, 5):
            x0 = 0 if i % 2 == 1 else 50
            obstacle = self.make_obstacles_I((x0, i * h_f), 3 * w_f - 40, 20)
            maze_obstacles.append(obstacle)
            obstacle = self.make_obstacles_I((5 * w_f + x0, i * h_f), 3 * w_f - 40, 20)
            maze_obstacles.append(obstacle)
        wall_1 = self.make_obstacles_I((3 * w_f, 0), 20, 4 * h_f + 20)
        maze_obstacles.append(wall_1)
        wall_2 = self.make_obstacles_I((5 * w_f - 20, h_f), 20, 4 * h_f)
        maze_obstacles.append(wall_2)
        rands = np.array([
            [0.544527, 0.144422],
            [0.985639, 0.9114],
            [0.561204, 0.896343],
            [0.252047, 0.453282],
            [0.82628, 0.520274],
            [0.314578, 0.168432],
            [0.754123, 0.0743171],
            [0.941966, 0.449393],
            [0.915798, 0.278299],
            [0.127793, 0.208063]])
        for i in range(1, 7):
            x = int((3.33 + rands[i][0]) * w_f)
            y = int(rands[i][1] * self.HEIGHT)
            obstacle = self.make_obstacles_I((x, y), 30, 30)
            maze_obstacles.append(obstacle)
        self.obstacles = maze_obstacles

    
    def make_obstacles(self):
        if self.level == 0:
            pass
        elif self.level == 1:
            self.generate_maze_I()
        elif self.level == 2:
            self.generate_inter_maze()
        elif self.level == 3:
            self.generate_complex_maze()
        return self.obstacles

    
    def draw_obstacles(self):
        '''Draw each side of the obstacles.'''
        obstacles = []
        for obstacle in self.obstacles:
            for side in obstacle:
                pygame.draw.rect(self.map, self.GRAY, side)
                obstacles.append(side)
        file = 'results/maps/map_level_' + str(self.level) + '.png'
        # if not os.path.exists(file):
        if True:
            map = pygame.Surface((self.WIDTH, self.HEIGHT))
            map.fill(self.WHITE)
            for obstacle in obstacles:
                color = self.GRAY
                pygame.draw.rect(map, color, obstacle)
            pygame.image.save(map, 'results/maps/map_level_' + str(self.level) + '.png')
        return obstacles


for level in range(4):
    env = Environment(map_dimensions=MAP_DIMENSIONS, level=level)
    env.make_obstacles()
    env.draw_obstacles()
