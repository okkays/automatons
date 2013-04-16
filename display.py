import pygame
from automatons import *
from sys import exit
from time import time
import os

class Display:
	"""Displays a grid of values"""

	def __init__(self, grid_size, update_interval, (width, height)=(640, 480), fullscreen=False):
		"""Set up the game"""
		pygame.init()
		if fullscreen:
			os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
			self.window = pygame.display.set_mode((0,0), pygame.NOFRAME)
		else:
			self.window = pygame.display.set_mode((width, height))
		self.window.fill((0, 0, 0))
		self.update_interval = update_interval
		self.agrid = AutomatonGrid(make_empty_grid(*grid_size), make_random_ruleset())
		self.paused = True
		self.make_board()

	def run(self):
		"""Start the main loop."""
		self.running = True
		self.board_time = time()
		while self.running:
			self.update()
			self.check_events()

	def update(self):
		"""Update objects on the screen."""
		self.update_board()
		pygame.display.flip()

	def update_board(self):
		"""Updates and blits the board."""
		if not self.paused and time() - self.board_time > self.update_interval:
			self.board_time = time()
			self.agrid.tick()
		self.window.blit(pygame.transform.scale(self.make_board(), 
				(self.window.get_width(), self.window.get_height())),
				(0,0))

	def make_board(self):
		"""Creates the next pygame board iteration."""
		board = pygame.Surface(
				(len(self.agrid.grid[0]) * 20, len(self.agrid.grid) * 20))
		for row in range(len(self.agrid.grid)):
			for col in range(len(self.agrid.grid[0])):
				if self.agrid.grid[row][col] == "1":
					if self.paused:
						cell_color = (0, 0, 150)
					else:
						cell_color = (0, 150, 0)
				else:
					if self.paused:
						cell_color = (0, 0, 255)
					else:
						cell_color = (0, 255, 0)
				pygame.draw.rect(board, cell_color,
						pygame.Rect(20 * col, 20 * row, 20, 20))
		return board

	def check_events(self):
		"""Check for user input"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_s:
					self.agrid.grid = make_empty_grid(len(self.agrid.grid), len(self.agrid.grid[0]))
				elif event.key == pygame.K_l:
					self.agrid.ruleset = make_ruleset_from_file('rules.txt')
				elif event.key == pygame.K_r:
					self.agrid.ruleset = make_random_ruleset()
				elif event.key == pygame.K_SPACE:
					self.paused = not self.paused
				elif event.key == pygame.K_o:
					with open("saved_rules.txt", "a") as f:
						f.write("======\n")
						f.writelines([k + v + "\n" for k, v in self.agrid.ruleset.iteritems()])
						f.write("======\n")

			elif event.type == pygame.MOUSEBUTTONDOWN:
				col = int((event.pos[0] / float(self.window.get_width())) * (len(self.agrid.grid[0])))
				row = int((event.pos[1] / float(self.window.get_height())) * (len(self.agrid.grid)))
				if self.agrid.grid[row][col] == "1":
					self.agrid.grid[row][col] = "0"
				else:
					self.agrid.grid[row][col] = "1"