import pygame
import math
from queue import PriorityQueue

WIDTH = 600 #size dimensions
WIN = pygame.display.set_mode((WIDTH, WIDTH)) #setting up display (visual)
pygame.display.set_caption("A* Path Finder")

RED = (255,0,0) #colors we need for the program
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node: #Part of setting up grid
	def __init__(self,row,col,width,sum_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.sum_rows = sum_rows

	def get_position(self):
		return self.row, self.col

	def is_visited(self):
		return self.color == RED

	def is_edge(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_goal(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_visited(self):
		self.color = RED

	def make_edge(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_goal(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid): #Check up, down, left, right and see if they are barriers
		self.neighbors = []
		if self.row < self.sum_rows - 1 and not grid[self.row +1][self.col].is_barrier(): #Down
			self.neighbors.append(grid[self.row+1][self.col])
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #Up
			self.neighbors.append(grid[self.row - 1][self.col])
		if self.col < self.sum_rows - 1 and not grid[self.row][self.col+1].is_barrier(): #Right
			self.neighbors.append(grid[self.row][self.col+1])
		if self.col > 0 and not grid[self.row][self.col -1].is_barrier(): #Left
			self.neighbors.append(grid[self.row][self.col -1])

	def __lt__(self, other): #Comparing two nodes together
		return False

def create_path(prior_node, current_node, draw):
	while current_node in prior_node:
		current_node = prior_node[current_node]
		current_node.make_path()
		draw()

def heuristic(start, end):
	x1, y1 = start
	x2, y2 = end
	return abs(x1-x2)+abs(y1-y2)

def astar(draw, grid, start, goal):
	count = 0
	open_set = PriorityQueue() 
	open_set.put((0, count, start)) #add start node with f score into the priority queue
	prior_node = {} #What nodes came from where
	g_score = {node: float("inf") for row in grid for node in row} #Every key starts at infinity and were using list comprehension
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row} #Every key starts at infinity and were using list comprehension
	f_score[start] = heuristic(start.get_position(), goal.get_position()) #F score is the heuristic or the distance from the start node to end node

	open_set_hash = {start} #Is node in the priority queue or not? Keeps track of items in queue and not in queue
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #Need a way to exist in case something goes wrong in alg
				pygame.quit()
		current_node = open_set.get()[2]
		open_set_hash.remove(current_node)
		if current_node == goal:
			create_path(prior_node, goal, draw)
			goal.make_goal()
			return True #making the shortest path
		for neighbor in current_node.neighbors:
			temp_g = g_score[current_node]+1
			if temp_g < g_score[neighbor]: #If we have found path to reach neightbor, we should update this path
				prior_node[neighbor] = current_node #What node did we come from?
				g_score[neighbor] = temp_g
				f_score[neighbor] = temp_g + heuristic(neighbor.get_position(), goal.get_position())
				if neighbor not in open_set_hash:
					count+=1
					open_set.put((f_score[neighbor], count, neighbor)) #Now we put in this new neighbor because it has a better path
					open_set_hash.add(neighbor) #We only store the node in here not f score
					neighbor.make_edge() #

		draw()
		if current_node != start:
			current_node.make_visited()

	return False



def create_grid(rows, width): #Going to be a square so colunmns and length dont matter
	grid = []
	gap = width // rows #Width for each node
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows) #Create a node 
			grid[i].append(node)

	return grid

def draw_grid(win, rows, width): #Just draws the lines between nodes
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i*gap),(width, i*gap)) #horizontal lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j*gap, 0),(j*gap, width)) #vertical lines

def draw(win, grid, rows, width): #Draws everything else
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_position(position, rows, width):
	gap = width // rows
	y,x = position

	row = y //gap
	col = x//gap
	return row, col

def main(win, width):
	ROWS = 50
	grid = create_grid(ROWS, width)
	start = None
	goal = None

	run = True
	started = False
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get(): #checking events
			if event.type == pygame.QUIT: #quit
				run = False

			if started:
				continue

			if pygame.mouse.get_pressed()[0]: #LEFT 
				position = pygame.mouse.get_pos()
				row, col = get_clicked_position(position, ROWS, width)
				node = grid[row][col]
				if not start and node != goal:
					start = node
					start.make_start()
				elif not goal and node != start:
					goal = node
					goal.make_goal()
				elif node != goal and node != start:
					node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #RIGHT
				position = pygame.mouse.get_pos()
				row, col = get_clicked_position(position, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == goal:
					goal = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and goal:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					astar(lambda: draw(win, grid, ROWS, width), grid, start, goal) #Lambda is an anonymous function, passing draw function as an argument to another function, helpful
				if event.key == pygame.K_c:
					start = None
					goal = None
					grid = create_grid(ROWS, width)
	pygame.quit()

main(WIN, WIDTH)











