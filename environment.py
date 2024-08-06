import pygame

class Environment():
	"""
	A class of the map where the robot will be moving around.

	Attributes
	----------
	dimensions : tuple
		The X and Y window dimensions.
	"""
	
	def __init__(self, map_dimensions):
		# Colors 
		self.WHITE = (255, 255, 255)
		self.BLACK = (0, 0, 0)
		self.RED = (255, 0, 0)
		self.GREEN = (0, 255, 0)
		self.BLUE = (0, 0, 255)
		self.BROWN = (189, 154, 122)
		self.YELLOW = (255, 255, 0)
		self.GRAY = (105, 105, 105)

		# Map dimensions
		self.WIDTH, self.HEIGHT = map_dimensions

		# Window settings
		self.FPS = 120
		pygame.display.set_caption('PRM')
		self.map = pygame.display.set_mode(size=(self.WIDTH, self.HEIGHT))
		self.map.fill(self.WHITE)

		self.obstacles = []
		

	def make_obstacles_T(self, initial_point):
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
		width, height = 50, 150

		side1 = pygame.Rect(x, y, height, width)
		side2 = pygame.Rect((x+height//2) - width//2, y, width, height)

		obstacle = [side1, side2]

		return obstacle

	def make_obstacles_L(self, initial_point):
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
		width, height = 50, 150

		side1 = pygame.Rect(x, y, width, height)
		side2 = pygame.Rect(x, y+height-width, height, width)

		obstacle = [side1, side2]

		return obstacle

	def make_obstacles_I(self, initial_point):
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
		width, height = 50, 150

		side1 = pygame.Rect(x, y, width, height)

		obstacle = [side1]

		return obstacle

	def make_obstacles_M(self, initial_point):
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
		width, height = 150, 150

		# Create rectangles for the letter 'M'
		side1 = pygame.Rect(x, y, width // 4, height)  # Left vertical line
		side2 = pygame.Rect(x + width // 2 - width // 12, y, width // 4, height)  # Middle vertical line
		side3 = pygame.Rect(x + width - width // 6, y, width // 4, height)  # Right vertical line
		side4 = pygame.Rect(x + width // 6, y , width - width // 3,
							height // 4)  # Middle horizontal line

		obstacle = [side1, side2, side3, side4]

		return obstacle

	def make_obstacles(self):
		"""Generate the obstacles to be placed on the final map to read MIT."""
		obstacle1 = self.make_obstacles_M(initial_point=(75 , 150))
		obstacle2 = self.make_obstacles_I(initial_point=(300, 150))
		obstacle3 = self.make_obstacles_T(initial_point=(425, 150))


		self.obstacles.append(obstacle1)
		self.obstacles.append(obstacle2)
		self.obstacles.append(obstacle3)

		return self.obstacles

	def draw_obstacles(self):
		"""Draw each side of the obstacles."""
		obstacles = []

		for obstacle in self.obstacles:
			for side in obstacle:
				pygame.draw.rect(surface=self.map, color=self.GRAY,
					rect=side)
				obstacles.append(side)

		return obstacles				