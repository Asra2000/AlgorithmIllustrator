import pygame
import math
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* path finding algorithm")

RED = (255,0, 0) 
GREEN = (0,255, 0) 
BLUE = (0,0, 255) 
YELLOW = (255,255, 0) 
WHITE = (255,255, 255) 
PURPLE = (255,0, 255)
BLACK = (0, 0, 0)
ORANGE = (255,165, 0) 
GREY = (128,128, 128)
TURQUOISE = (64,224, 224) 

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = col * width
		self.y = row * width
		self.color = WHITE
		self.neighbours = []
		self.width = WIDTH
		self.total_rows = total_rows

	def get_pos(self):
		return self.col, self.row

	def is_visited(self):
		return self.color == RED

	def is_open(self):
		return self.color == WHITE

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color ==  ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE
	def make_start(self):
		self.color = ORANGE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbours(self, grid):
		self.neighbours = []

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
			self.neighbours.append(grid[self.row + 1][self.col]) 
		if self.row > 0  and not grid[self.row - 1][self.col].is_barrier(): # up
			self.neighbours.append(grid[self.row - 1][self.col])
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
			self.neighbours.append(grid[self.row][self.col+1])
		if self.col > 0 and not grid[self.row][self.col -1].is_barrier(): # left
			self.neighbours.append(grid[self.row][self.col - 1])		

	def __lt__(self, other):
		return False

# heuristic func
def h(p1, p2):
	d = ((p1[0]-p2[0])**2+ (p1[1]-p2[1])**2)**0.5
	return d

def make_grid(rows, width):
	grid = []
	gap = width//rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	f_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score[start] = h((start.get_pos()), (end.get_pos()))

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			while current != start:
				current = came_from[current]
				current.make_path()
			return True
		for neighbour in current.neighbours:
			temp_g_score = g_score[current]
			if temp_g_score < g_score[neighbour]:
				came_from[neighbour]  = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()
		draw()

		if current != start:
			current.make_closed()

	return False

def draw_grid(win, rows, width):
	gap = width//rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
		pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, width))

def draw(win, grid, rows, width):
	win.fill(BLACK)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


# position on grid being clicked
def get_clicked_position(pos, rows, width):
	gap = width//rows
	x, y = pos

	row = y//gap
	col = x//gap

	return row, col

def main(win , width):
	pygame.init()
	ROWS = 50
	grid  = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	started = False
	while run:
		draw(WIN, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if started:
				continue

			if pygame.mouse.get_pressed()[0]: # left
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROWS, width)
				spot = grid[row][col]
				if not start:
					start = spot
					start.make_start()
				elif not end and spot != start:
					end = spot
					end.make_end()
				elif spot != start and spot != end:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # right
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					# start the algorithm
					for row in grid:
						for spot in row:
							spot.update_neighbours(grid)

					result  = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					if result == False:
						font = pygame.font.SysFont('comicsans', 32)
						text = font.render("Sorry, no path found", True, TURQUOISE)
						win.blit(text, (width//2, width//2))
						pygame.display.update()

				if event.key  == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)


	pygame.quit()

main(WIN, WIDTH)
