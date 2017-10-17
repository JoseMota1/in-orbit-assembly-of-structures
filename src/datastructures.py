from collections import namedtuple, deque # lista imutavel com acesso hash , lista duplamente ligada
from itertools import combinations

Vertice = namedtuple('Vertice', ['id', 'weight']) 
Launch = namedtuple('Launch', ['date', 'payload', 'fixed_cost', 'variable_cost'])

class Frontier:
	def __init__(self):
		self.queue = list()
		self.visited = dict()

	def insert(self, node):
		if not visited[node.state]
			heapq.heappush(self.queue, node)
			visited[node.state] = node
		if visited[node]
			if node.cost < visited[node].cost
				heapq.heappush(self.queue, node)

	def pop(self):
		while True:
			node = heapq.heappop(self.queue)
			if not visited[node]:
				return node




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

	__slots__ = ('land', 'air', 'date')
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
		max_payload = self.launches[state.date].max_payload #estamos a assumir um unico lançamento por data
		
		# TODO still need to check weight
		actions = []
		nvertices = 3 # better checking TODO
		for vertice in land:
			# actions.append('load' + vertice.id)
			connections = (v for v in edges[vertice] if v not in air)
			[actions.append( 'load ' + vertice.id + ' ' +  str(vs)) for n in range(nvertices+1) for vs in combinations(connections, n) if vs if sum(v.weight for v in vs) < max_payload]
			
		return actions
		