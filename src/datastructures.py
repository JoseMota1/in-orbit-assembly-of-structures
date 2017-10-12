from collections import namedtuple
from collections import deque

Vertice = namedtuple('Vertice', ['id', 'weight'])

class Edge:
	__slots__ = ('v1', 'v2')
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		
	def __repr__(self):
		return ('Edge with V1: ' + str(self.v1) + ' and V2: ' + str(self.v2))


class Launch:
	__slots__ = ('date', 'max_payload', 'fixed_cost', 'variable_cost')
	def __init__(self, date, max_payload, fixed_cost, variable_cost):
		self.date = date
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.variable_cost = variable_cost
		
	def __repr__(self):
		return ('Launch date: ' + self.date + ', max_payload: ' + str(self.max_payload) + 
			', fixed_cost: ' + str(self.fixed_cost) + 
			', variable_cost: ' + str(self.variable_cost))
		
		
class Node:
	__slots__ = ('state', 'cost', 'parent', 'operator')
	def __init__(self, state, cost, parent, operator):
		self.state = state
		self.cost = cost
		self.parent = parent
		self.operator = operator