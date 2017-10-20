from collections import namedtuple, deque, OrderedDict # lista imutavel com acesso hash , lista duplamente ligada
from itertools import combinations

Vertice = namedtuple('Vertice', ['id', 'weight'])
loaded = namedtuple('loaded', ['weight', 'vertices'])

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
	__slots__ = ('date', 'max_payload', 'fixed_cost', 'variable_cost', 'next_launch')
	def __init__(self, date, max_payload, fixed_cost, variable_cost, next_launch):
		self.date = date
		self.max_payload = max_payload
		self.fixed_cost = fixed_cost
		self.variable_cost = variable_cost
		self.next_launch = next_launch

	def __repr__(self):
		return ('Launch date: ' + str(self.date) +
			', max_payload: ' + str(self.max_payload) +
			', fixed_cost: ' + str(self.fixed_cost) +
			', variable_cost: ' + str(self.variable_cost) +
			', next_launch: ' + str(self.next_launch))


class State:
	__slots__ = ('land', 'loaded', 'air', 'date')
	def __init__(self, land, loaded, air, date):
		self.land = land
		self.loaded = loaded
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

		actions = []
		if not self.state.loaded.vertices:
			action.append('pass')
		elif (len(self.state.loaded.vertices) > 1 or
			len(self.state.loaded.vertices) == 1 and any(self.edges[self.state.loaded.vertices]) in self.state.air):
			actions.append('launch')
		[actions.append(vertice.id) for vertice in self.state.land
			if self.loaded.weight + vertice.weight < max_payload
			if any(self.edges[vertice]) in self.state.air + self.state.loaded.vertices or not self.state.air]

		return actions


	def costfunction(self, action): # VER COMO ESTA ESCRITO
		if action[0] == 'pass':
			cost = 0

		if action[0] == 'launch':
			for line in Launch:
				fixedcost = line[2] 
				variablecost = line[3]
				SI = len(self.state.loaded.vertices) 
				cost = fixedcost+SI*variablecost 


		return cost

	def result(pstate, action): # VER COMO ESTA ESCRITO
		if action[0] == 'pass':
			for line in Launch:
				pstate.date = line[4]    

		if action[0] == 'launch':
			pstate.air.append(pstate.loaded)
			pstate.land.remove(pstate.loaded) 
			pstate.loaded.clear()

		return


	def childnode(self, parent, action): # VER COMO ESTA ESCRITO
		action_cost = costfunction(action)
		result(parent.state, action)

		return 
