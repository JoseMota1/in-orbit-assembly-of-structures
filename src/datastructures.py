from collections import namedtuple, deque

Vertice = namedtuple('Vertice', ['id', 'weight'])
Launch = namedtuple('Launch', ['date', 'payload', 'fixed_cost', 'variable_cost'])

class Launch:
	__slots__ = ('date', 'max_payload', 'fixed_cost', 'variable_cost')
	def __init__(self, date, max_payload, fixed_cost, variable_cost):
		self.date = date
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.variable_cost = variable_cost
		
	def __repr__(self):
		return ('Launch date: ' + self.date + 
			', max_payload: ' + str(self.max_payload) + 
			', fixed_cost: ' + str(self.fixed_cost) + 
			', variable_cost: ' + str(self.variable_cost))
		
		
class State:
	
	def __init__(self, land, air, date):
		self.land = land
		self.air = air
		self.date = date
		
	
class Node:
	__slots__ = ('state', 'cost', 'parent', 'action')
	def __init__(self, state, cost, parent, action):
		self.state = state
		self.parent = parent
		self.action = action
		self.cost = cost
		
		
class Problem:
	
	def __init__(self, vertices, edges, launches):
		self.vertices = vertices
		self.edges = edges
		self.launches = launches		
		
	def actions(self, state):