import pygame
import math
from queue import SimpleQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# colors
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

class Node(object):
	def __init__(self,row, col, width):
		self.row = row
		self.col = col
		self.x = col * width 
		self.y = row * width 
		self.width = width
		self.neighbour = []
		self.color = WHITE
		self.visited = False
		self.parent = None

	def get_pos(self):
		return self.col, self.row

	def get_cor(self):
		return (self.x + self.width// 2, self.y + self.width//2)

	def make_start(self):
		self.color = GREEN 

	def make_black(self):
		self.color = BLACK

	def make_grey(self):
		self.color = GREY

	def make_red(self):
		self.color = RED

	def make_end(self):
		self.color = TURQUOISE
	
	def add_neighbour(self):
		pass

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


def make_grid(rows, width):
	grid = []
	gap = width//rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Node(i, j, gap)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width//rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
		pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, width))



def draw(win, nodes, edges, start, end, making_edge, path_found):
	win.fill(WHITE)
	if not making_edge:
		draw_grid(win, 20, WIDTH)
	if start:
		start.draw(win)
	if end:
		end.draw(win)
	for node in nodes:
		node.draw(win)
	for edge in edges:
		if len(edge) == 2:
			pygame.draw.line(win, GREEN, edge[0].get_cor(), edge[1].get_cor())
	if path_found:
		node = end
		node.make_red()
		while node != start:
			pygame.draw.line(win, RED, node.get_cor(), node.parent.get_cor())
			node = node.parent
			node.make_red()
	pygame.display.update()

def get_clicked_position(pos, rows, width):
	gap = width//rows
	x, y = pos

	row = y//gap
	col = x//gap

	return row, col

def algorithm(start, end, edges, win):
	start.visited = True
	queue = SimpleQueue()
	queue.put(start)

	while not queue.empty():
		node = queue.get()
		if node != end:
			for edge in edges:
				if node == edge[0]:
					if not edge[1].visited:
						queue.put(edge[1])
						edge[1].parent = node
						edge[1].visited = True
				elif node == edge[1]:
					if not edge[0].visited:
						queue.put(edge[0])
						edge[0].parent = node
						edge[0].visited = True

			node.make_grey()
		else:
			end.make_grey()
			return True

	return False



def main(win, ROW):
	pygame.init()
	nodes = []
	edges = []
	grid = make_grid(ROW, WIDTH)
	path_found = False

	start = None
	end = None
	edge = []
	making_edge = False
	started = False

	run = True
	while run:
		draw(win, nodes, edges, start, end, making_edge, path_found)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if started:
				continue

			if not making_edge and pygame.mouse.get_pressed()[0]: # left
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROW, WIDTH)
				# new_node = Node(pos[0], pos[1], 10)
				new_node = grid[row][col]
				if start == None:
					start = new_node
					start.make_start()
				elif end == None and start and new_node != start:
					end = new_node
					end.make_end()
				elif end and start:
					if new_node != start and new_node != end:
						new_node.make_black()
						nodes.append(new_node)

			if making_edge and pygame.mouse.get_pressed()[0]: # edges
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROW, WIDTH)
				new_node = grid[row][col]
				if new_node in nodes or new_node == start or new_node == end and new_node not in edge:
					edge.append(new_node)
				if len(edge) == 2:
					if edge not in edges and list((edge[1], edge[0])) not in edges:
						edges.append(edge)
					elif edge in edges:
						edges.remove(edge)
					else:
						edges.remove(list((edge[1], edge[0])))
					edge = []


			if event.type == pygame.KEYDOWN:
				if event.key  == pygame.K_e:
					making_edge = not making_edge 

				if event.key == pygame.K_SPACE:
					started = True
					path_found = algorithm(start, end, edges, win)
					started = False

				if event.key == pygame.K_c:
					edges = []
					nodes = []
					path_found = False
					start = None
					end = None
					edge = []
					making_edge = False


	pygame.quit()

main(WIN, 20)