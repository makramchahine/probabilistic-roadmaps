import pygame
import random
import os

POSI = [[436, 227],
[424, 333],
[103, 240],
[379, 170],
[116, 247],
[206, 300],
[60, 152],
[527, 218],
[121, 329],
[44, 167],
[456, 114],
[196, 253],
[442, 236],
[565, 278],
[317, 215],
[308, 300],
[572, 82],
[567, 203],
[437, 189],
[56, 324],
[568, 113],
[300, 135],
[314, 334],
[258, 136],
[245, 162],
[378, 137],
[413, 303],
[167, 303],
[65, 82],
[406, 226],
[531, 215],
[423, 322],
[171, 311],
[289, 127],
[541, 213],
[262, 218],
[387, 96],
[92, 113],
[69, 230],
[60, 240],
[142, 105],
[188, 221],
[109, 159],
[515, 269],
[268, 175],
[412, 173],
[360, 240],
[275, 265],
[27, 180],
[115, 117],
[96, 269],
[512, 274],
[243, 260],
[152, 179],
[366, 194],
[480, 322],
[47, 327],
[450, 335],
[199, 118],
[562, 106],
[55, 233],
[171, 316],
[416, 138],
[286, 207],
[321, 224],
[11, 99],
[549, 83],
[312, 325],
[46, 181],
[476, 277],
[177, 263],
[24, 112],
[568, 135],
[481, 147],
[41, 196],
[117, 207],
[200, 119],
[254, 140],
[243, 320],
[45, 107],
[549, 140],
[328, 158],
[150, 119],
[450, 285],
[101, 297],
[108, 238],
[134, 221],
[177, 109],
[464, 271],
[112, 198],
[46, 311],
[566, 206],
[506, 267],
[47, 110],
[356, 92],
[119, 241],
[97, 272],
[308, 283],
[505, 239],
[441, 92]
]

INIT = [[35, 50],
	   [46, 39],
	   [57, 38],
	   [47, 50],
	   [51, 35],
	   [24, 24],
	   [31, 37],
	   [20, 29],
	   [59, 31],
	   [40, 31],
	   [56, 36],
	   [41, 53],
	   [40, 37],
	   [51, 28],
	   [34, 44],
	   [50, 26],
	   [53, 36],
	   [43, 55],
	   [21, 46],
	   [38, 40],
	   [53, 36],
	   [29, 41],
	   [23, 40],
	   [28, 34],
	   [35, 47],
	   [32, 48],
	   [52, 21],
	   [39, 56],
	   [42, 25],
	   [27, 51],
	   [52, 40],
	   [40, 47],
	   [53, 21],
	   [39, 35],
	   [56, 44],
	   [51, 32],
	   [20, 45],
	   [29, 52],
	   [24, 60],
	   [28, 46],
	   [39, 24],
	   [36, 31],
	   [45, 24],
	   [55, 25],
	   [46, 24],
	   [54, 51],
	   [30, 30],
	   [24, 58],
	   [38, 55],
	   [21, 41],
	   [29, 29],
	   [29, 54],
	   [54, 60],
	   [53, 32],
	   [57, 21],
	   [20, 34],
	   [42, 22],
	   [47, 55],
	   [54, 25],
	   [24, 31],
	   [51, 20],
	   [28, 60],
	   [21, 20],
	   [39, 47],
	   [26, 20],
	   [58, 42],
	   [54, 21],
	   [45, 41],
	   [35, 22],
	   [60, 51],
	   [48, 23],
	   [20, 29],
	   [52, 23],
	   [33, 31],
	   [46, 57],
	   [47, 56],
	   [48, 44],
	   [53, 58],
	   [52, 37],
	   [21, 34],
	   [49, 23],
	   [38, 60],
	   [54, 24],
	   [32, 56],
	   [52, 29],
	   [38, 50],
	   [34, 57],
	   [35, 50],
	   [20, 58],
	   [45, 56],
	   [54, 45],
	   [35, 37],
	   [51, 42],
	   [27, 35],
	   [27, 31],
	   [51, 23],
	   [34, 43],
	   [33, 22],
	   [59, 57],
	   [30, 28]]

class Environment():
	"""
	A class of the map where the robot will be moving around.

	Attributes
	----------
	dimensions : tuple
		The X and Y window dimensions.
	"""
	
	def __init__(self, map_dimensions, level=1):
		# Colors 
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

		# Map dimensions
		self.WIDTH, self.HEIGHT = map_dimensions

		# Window settings
		self.FPS = 120
		pygame.display.set_caption('PRM')
		self.map = pygame.display.set_mode(size=(self.WIDTH, self.HEIGHT))
		self.map.fill(self.WHITE)

		self.level = level

		self.obstacles = []
		

	def make_obstacles_T(self, initial_point, width=50, height=150):
		"""
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
		"""
		x, y = initial_point[0], initial_point[1]

		side1 = pygame.Rect(x, y, height, width)
		side2 = pygame.Rect((x+height//2) - width//2, y, width, height)

		obstacle = [side1, side2]

		return obstacle

	def make_obstacles_L(self, initial_point, width=50, height=150):
		"""
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
		"""	
		x, y = initial_point[0], initial_point[1]

		side1 = pygame.Rect(x, y, width, height)
		side2 = pygame.Rect(x, y+height-width, height, width)

		obstacle = [side1, side2]

		return obstacle

	def make_obstacles_I(self, initial_point, width=50, height=150):
		"""
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
		"""
		x, y = initial_point[0], initial_point[1]

		side1 = pygame.Rect(x, y, width, height)

		obstacle = [side1]

		return obstacle

	def make_obstacles_M(self, initial_point, width=150, height=150):
		"""
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
		"""
		x, y = initial_point[0], initial_point[1]

		# Create rectangles for the letter 'M'
		side1 = pygame.Rect(x, y, width // 4, height)  # Left vertical line
		side2 = pygame.Rect(x + width // 2 - width // 12, y, width // 4, height)  # Middle vertical line
		side3 = pygame.Rect(x + width - width // 6, y, width // 4, height)  # Right vertical line
		side4 = pygame.Rect(x + width // 6, y , width - width // 3,
							height // 4)  # Middle horizontal line

		obstacle = [side1, side2, side3, side4]

		return obstacle

	def make_obstacle_C(self, initial_point, width=50, height=150):
		"""
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
        """
		x, y = initial_point

		# Calculate thickness as a reasonable ratio of height (e.g., 1/6th of the height)
		thickness = max(1, height // 3)

		# Left vertical side
		side1 = pygame.Rect(x, y, thickness, height)

		# Top horizontal side
		side2 = pygame.Rect(x, y, width, thickness)

		# Bottom horizontal side
		side3 = pygame.Rect(x, y + height - thickness, width, thickness)

		obstacle = [side1, side2, side3]

		return obstacle

	def generate_maze_I(self):
		"""
        Generate a maze-like environment with 'I' shaped obstacles restricted to the middle 2/3rds of the map vertically.
        """
		maze_obstacles = []
		spacing = 10  # Space between obstacles
		obstacle_width = 60
		obstacle_height = 60

		decal = 5
		decaf = 20

		# Calculate boundaries for the middle 2/3rds of the map
		y_min = self.HEIGHT // 6
		y_max = 5 * self.HEIGHT // 6

		# Adding random elements within the middle 2/3rds
		for i in range(40):  # Add some random obstacles
			x = POSI[i+decal][0]
			y = POSI[i+decal][1]
			obstacle = self.make_obstacles_I(initial_point=(x, y), width=INIT[i+decaf][0], height=INIT[i+decaf][1])
			maze_obstacles.append(obstacle)

		self.obstacles = maze_obstacles



	def make_obstacles(self):
		if self.level == 0:
			# Environment 0: no obstacles
			pass

		if self.level == 1:
			obstacle1 = self.make_obstacles_M(initial_point=(75, 140))
			obstacle2 = self.make_obstacles_I(initial_point=(300, 200))
			obstacle3 = self.make_obstacles_L(initial_point=(425, 160))


			self.obstacles.append(obstacle1)
			self.obstacles.append(obstacle2)
			self.obstacles.append(obstacle3)

		elif self.level == 2:
			# Environment 3: Add a different set of obstacles
			obstacle1 = self.make_obstacles_T(initial_point=(25, 200), width=50, height=120)
			obstacle2 = self.make_obstacles_L(initial_point=(190, 120), width=60, height=80)
			obstacle3 = self.make_obstacles_I(initial_point=(350, 100), width=50, height=120)
			obstacle4 = self.make_obstacles_M(initial_point=(450, 220), width=140, height=140)
			obstacle5 = self.make_obstacle_C(initial_point=(250, 270), width=100, height=100)

			self.obstacles.append(obstacle1)
			self.obstacles.append(obstacle2)
			self.obstacles.append(obstacle3)
			self.obstacles.append(obstacle4)
			self.obstacles.append(obstacle5)

		elif self.level == 3:
			self.generate_maze_I()

		return self.obstacles

	def draw_obstacles(self):
		"""Draw each side of the obstacles."""
		obstacles = []

		for obstacle in self.obstacles:
			for side in obstacle:
				pygame.draw.rect(surface=self.map, color=self.GRAY,
					rect=side)
				obstacles.append(side)

		# save a png file of the map without the start and goal positions if it doesn't exist under 'results/maps/map_level_'+str(self.level)+'.png'
		file = 'results/maps/map_level_'+str(self.level)+'.png'
		if not os.path.exists(file):
			map = pygame.Surface((self.WIDTH, self.HEIGHT))
			map.fill(self.WHITE)
			for obstacle in obstacles:
				color = random.choice([self.GREEN, self.RED, self.BLUE, self.ORANGE, self.PURPLE])
				pygame.draw.rect(map, color, obstacle)
			pygame.image.save(map, 'results/maps/map_level_'+str(self.level)+'.png')

		return obstacles				