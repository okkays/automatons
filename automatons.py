from time import sleep
from random import randint
from copy import deepcopy
import sys

def make_empty_grid(rows, cols):
	"""Makes a new grid full of 0s"""
	return [["0"]*cols for col in range(0,rows)]

# def make_random_grid(rows, cols):
# 	return [[str(randint(0,1))]*cols for y in range(0,rows)]

def make_random_ruleset():
	"""Generates a random 5-length ruleset"""
	rules = ['0'*(5 - (len(str(bin(i))) - 2)) + str(bin(i))[2:] for i in range(0, 32)]
	ruleset = dict()
	for rule in rules:
		ruleset[rule[0:5]] = str(randint(0,1))
	return ruleset

def make_ruleset_from_file(filename):
	"""Loads a ruleset from a rule file"""
	with open(filename) as f:
		rules = f.read().splitlines()
	ruleset = dict()
	for rule in rules:
		ruleset[rule[:5]] = rule[5]
	return ruleset

class AutomatonGrid(object):
	
	def __init__(self, grid, ruleset):
		self.grid = grid
		self.ruleset = ruleset

	def compute_rule(self, row, col):
		rule = str()
		#up
		if row == len(self.grid) - 1:
			rule += self.grid[0][col]
		else:
			rule += self.grid[row + 1][col]
		#left
		if col == len(self.grid[0]) - 1:
			rule += self.grid[row][0]
		else:
			rule += self.grid[row][col + 1]
		#down
		if row == 0:
			rule += self.grid[len(self.grid) - 1][col]
		else:
			rule += self.grid[row - 1][col]
		#right
		if col == 0:
			rule += self.grid[row][len(self.grid[0]) - 1]
		else:
			rule += self.grid[row][col - 1]
		#middle
		rule += self.grid[row][col]
		return rule

	def tick(self):
		next_grid = deepcopy(self.grid)
		for row in range(0, len(self.grid)):
			for col in range(0, len(self.grid[0])):
				next_grid[row][col] = self.ruleset[self.compute_rule(row, col)]
		self.grid = next_grid

	# def update_term(self.grid):
	# 	out_string = str()
	# 	for row in grid:
	# 		out_string += "\n"
	# 		for item in row:
	# 			if item == "0":
	# 				out_string += " "
	# 			if item == "1":
	# 				out_string += "+"
	# 	out_string += ("\n" + "=" * len(self.grid[0]))
	# 	sys.stdout.write(out_string)
