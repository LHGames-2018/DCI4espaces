import math
from collections import defaultdict

class AStarSolver:
	def __init__(self, Class, get_x = lambda object: object.x, get_y = lambda object: object.y):
		"""
		Create a new AStarSolver object.
		:param get_x: function that returns an object's horizontal position.
		:param get_y: function that returns an object's vertical position.
		"""
		self.Class = Class
		self.dimensions = [get_x, get_y]

	def solve(self, start, target):
		"""
		Python implementation of this pseudocode: https://en.wikipedia.org/wiki/A*_search_algorithm
		"""
		closed = [] 
		open = [start]
		came_from = {}

		g_score = defaultdict(lambda: math.inf)
		g_score[start] = 0

		f_score = defaultdict(lambda: math.inf)
		f_score[start] = self.heuristic(start, target)

		while len(open) > 0:
			open.sort(key = lambda node: f_score[node])
			current = open.pop(0)

			if current == target:
				return self.build_path(target, came_from)
						
			closed.append(current)

			for neighbor in self.neighbors(current, target):
				if neighbor in closed:
					continue
				
				current_g_score = g_score[current] + self.g_score(current, neighbor)
				
				if neighbor not in open:
					open.append(neighbor)
				elif current_g_score >= g_score[neighbor]:
					continue
				
				came_from[neighbor] = current
				g_score[neighbor] = current_g_score
				f_score[neighbor] = current_g_score + self.heuristic(neighbor, target)
		
		return None
	
	def build_path(self, target, came_from):
		"""
		Reconstruct the path to the target.
		"""
		path = []
		node = target

		while node in came_from:
			path.insert(0, node)
			node = came_from[node]
		
		return path
	
	def distance(self, start, target):
		"""
		Calculate the manhattan distance between two nodes.
		"""
		return sum(abs(d(target) - d(start)) for d in self.dimensions)

	def heuristic(self, start, target):
		"""
		Estimate the cost of getting to the target node.
		"""
		return self.distance(start, target)

	def g_score(self, start, target):
		"""
		Calculate the cost of getting to the target node.
		"""
		return self.distance(start, target)
	
	def neighbors(self, node, target):
		"""
		Generate a node's neighbors.
		"""
		for current_dimension in self.dimensions:
			previous = [d(node) - (1 if d == current_dimension else 0) for d in self.dimensions]
			next = [d(node) + (1 if d == current_dimension else 0) for d in self.dimensions]
			for neighbor in [self.Class(*previous), self.Class(*next)]:
				if self.is_valid_neighbor(neighbor) or neighbor == target:
					yield neighbor
	
	def is_valid_neighbor(self, node):
		"""
		Returns True if a node is a valid neighbor.
		"""
		return True