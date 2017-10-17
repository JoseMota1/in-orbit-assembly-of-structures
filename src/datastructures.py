from collections import namedtuple, deque, OrderedDict # lista imutavel com acesso hash , lista duplamente ligada
from itertools import combinations

Vertice = namedtuple('Vertice', ['id', 'weight'])
Launch = namedtuple('Launch', ['date', 'payload', 'fixed_cost', 'variable_cost'])

class Frontier:
	def __init__(self):
		self.queue = list()
		self.expanded = dict()

	def insert(self, node):
		if not expanded[node.state]:
			heapq.heappush(self.queue, node)
			expanded[node.state] = [node.cost, False]
		if expanded[node.state] and node.cost < expanded[node.state].cost:
			heapq.heappush(self.queue, node)
			expanded[node.state][0] = node.cost

	def pop(self):
		while True:
			node = heapq.heappop(self.queue)
			if not expanded[node.state][1]:
				expanded[node.state] = [node.cost, True]
				return node


class Launch:
	__slots__ = ('date', 'max_payload', 'fixed_cost', 'variable_cost')
	def __init__(self, date, max_payload, fixed_cost, variable_cost):
		self.date = date
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.variable_cost = variable_cost

	def __repr__(self):
		return ('Launch date: ' + str(self.date) +
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
		max_payload = self.launches[state.date].max_payload # Estamos a assumir um unico lançamento por data

		actions = ['pass']
		for vertice in state.land:
		
			weights = [vertice.weight]
			inair = []
			[inair.append(v) if v in state.air else weights.append(v.weight) for v in self.edges[vertice]]
			
			if any(inair):
				actions.append('load ' + vertice.id)
			
			minweight = min(weights)
			nvertices = round(max_payload/minweight)
			
			#for comb in combinations((v for v in self.edges[vertice] if v not in state.air), 3):
			#	print(comb)
			
			[actions.append( 'load ' + vertice.id + ' ' + ' '.join((v.id for v in vs)))
				for n in range(1, nvertices+1) 
				for vs in combinations((v for v in self.edges[vertice] if v not in state.air), n) 
				if vs if sum(v.weight for v in vs) < max_payload]
			
		return actions
		
	
	def result(pstate, action):
		action1 = action.split(' ')
		if action1[0] == 'pass':
			pstate.date = min()
			
		return pstate

	def childnode(self, parent, action):
	
		
		state = result(parent.state, action)
		parent = parent
		action = action
		cost = parent.cost + costfunction(action)
		
		return Node(state, parent, action, cost)
		