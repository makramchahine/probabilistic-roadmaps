import pygame

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
		width, height = 50, 150

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
		thickness = max(1, height // 6)

		# Left vertical side
		side1 = pygame.Rect(x, y, thickness, height)

		# Top horizontal side
		side2 = pygame.Rect(x, y, width, thickness)

		# Bottom horizontal side
		side3 = pygame.Rect(x, y + height - thickness, width, thickness)

		obstacle = [side1, side2, side3]

		return obstacle

	def make_obstacles(self):
		if self.level == 0:
			# Environment 0: no obstacles
			pass

		if self.level == 1:
			obstacle1 = self.make_obstacles_M(initial_point=(75 , 140))
			obstacle2 = self.make_obstacles_I(initial_point=(300, 200))
			obstacle3 = self.make_obstacles_L(initial_point=(425, 160))


			self.obstacles.append(obstacle1)
			self.obstacles.append(obstacle2)
			self.obstacles.append(obstacle3)


		elif self.level == 2:
			# Environment 2: same as 1 with larger obstacles
			obstacle1 = self.make_obstacles_L(initial_point=(50, 140), width=75, height=200)
			obstacle2 = self.make_obstacles_M(initial_point=(300, 100), width=200, height=200)
			obstacle3 = self.make_obstacles_I(initial_point=(550, 160), width=130, height=400)

			self.obstacles.append(obstacle1)
			self.obstacles.append(obstacle2)
			self.obstacles.append(obstacle3)


		elif self.level == 3:
			# Environment 3: Add a different set of obstacles
			obstacle1 = self.make_obstacles_T(initial_point=(25, 200), width=50, height=120)
			obstacle2 = self.make_obstacles_L(initial_point=(180, 150), width=60, height=130)
			obstacle3 = self.make_obstacles_I(initial_point=(350, 100), width=100, height=200)
			obstacle4 = self.make_obstacles_M(initial_point=(450, 220), width=60, height=180)

			self.obstacles.append(obstacle1)
			self.obstacles.append(obstacle2)
			self.obstacles.append(obstacle3)
			self.obstacles.append(obstacle4)

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