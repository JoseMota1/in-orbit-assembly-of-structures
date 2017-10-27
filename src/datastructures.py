# lista imutavel com acesso hash , lista duplamente ligada e dicionario ordenado
from collections import namedtuple, deque, OrderedDict
from itertools import combinations, islice
from copy import deepcopy, copy
from heapq import heappush, heappop
from time import perf_counter

Vertice = namedtuple('Vertice', ['name', 'weight'])

class Frontier:
	def __init__(self, node):
		""" Frontier class is initialized with an initial Node.
		The expanded dictionary contains the expanded nodes as keys, and
		the cost of each as value
		"""
		self.queue = list()
		self.expanded = dict()
		self.insert(node)

	def insert(self, node):
		if not self.expanded.get(node.state, False):
			heappush(self.queue, node)
			self.expanded[node.state] = [node.pathcost, False]
		elif node.pathcost < self.expanded[node.state][0]:
			print('Replace')
			heappush(self.queue, node)
			self.expanded[node.state][0] = node.pathcost

	def pop(self):
		while self.queue:
			node = heappop(self.queue)
			if not self.expanded[node.state][1]:
				self.expanded[node.state] = [node.pathcost, True]
				return node

	def isempty(self):
		""" TODO SHIT """
		if not self.queue:
			return True
		return False


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

	def __repr__(self):
		return ('State LAND ' + str(self.land) +
			' LOADED ' + str(self.loaded) +
			' AIR ' + str(self.air) +
			' DATE ' + str(self.date))


class Node:
	__slots__ = ('state', 'parent', 'action', 'pathcost', 'cost')

	def __init__(self, state, parent, action, pathcost, cost):
		self.state = state
		self.parent = parent
		self.action = action
		self.pathcost = pathcost
		self.cost = cost

	def __repr__(self):
		return ('Node with ' + str(self.state) +
			#' from Parent ' + str(self.parent) +
			#' with action: ' + str(self.action) +
			' and cost ' + str(self.cost))

	def __lt__(self, other):
		return self.cost < other.cost


class Problem:
	HEURISTIC = False

	def __init__(self, vertices, edges, launches):
		self.vertices = vertices
		self.edges = edges
		self.launches = launches

	def initialnode(self):
		date = next(islice(self.launches, 1))
		state = State(frozenset(self.vertices.values()), frozenset(), frozenset(), str(date))
		parent = False
		action = False
		pathcost = 0
		if self.HEURISTIC:
			cost = pathcost + self.hcost(state, action)
		else:
			cost = pathcost

		return Node(state, parent, action, pathcost, cost)

	def goal(self, state):
		if not state.land | state.loaded:
			return True
		return False

	def actions(self, state):
		actions = []

		# We are assuming that the launch date is an unique id
		launch = self.launches.get(state.date, 0)
		if launch:
			max_payload = launch.max_payload
		else:
			return actions

		if not state.loaded:
			actions.append('pass')
		elif ( (len(state.loaded) > 1) or
				(len(state.loaded) == 1
					and any(edge in state.air for edge in self.edges[next(iter(state.loaded))]) ) or
				(len(state.loaded) == 1 and not state.air) ):
			actions.append('launch')
		[actions.append(vertice) for vertice in state.land
			if sum(vertice.weight for vertice in state.loaded) + vertice.weight <= max_payload
			if not state.air | state.loaded or
			not state.loaded and any(edge in state.air for edge in self.edges[vertice]) or
			any(edge in state.loaded | state.air for edge in self.edges[vertice])]

		return actions

	def childnode(self, parent, action):
		pstate = parent.state

		if action == 'pass':
			date = self.launches[pstate.date].next_launch
			state = State(frozenset(pstate.land), frozenset(pstate.loaded), frozenset(pstate.air), date)
			pathcost = parent.pathcost
			if self.HEURISTIC:
				cost = pathcost + self.hcost(state, action)
			else:
				cost = pathcost

		elif action == 'launch':
			air = pstate.air | pstate.loaded
			date = self.launches[pstate.date].next_launch
			state = State(frozenset(pstate.land), frozenset(), air, date)
			pathcost = parent.pathcost + self.launches[pstate.date].fixed_cost
			if self.HEURISTIC:
				cost = pathcost + self.hcost(state, action)
			else:
				cost = pathcost

		else: # action load Vertice
			land = set(pstate.land)
			land.remove(action)
			land = frozenset(land)
			loaded = set(pstate.loaded)
			loaded.add(action)
			loaded = frozenset(loaded)
			state = State(land, loaded, frozenset(pstate.air), pstate.date)
			pathcost = parent.pathcost + (
					self.launches[pstate.date].variable_cost *
					self.vertices[action.name].weight )
			if self.HEURISTIC:
				cost = pathcost + self.hcost(state, action)
			else:
				cost = pathcost

		return Node(state, parent, action, pathcost, cost)

	def heuristics(self):
		self.HEURISTIC = True

		vertices = frozenset(self.vertices.values())
		self.verticesweight = dict()
		for i in range(len(vertices)+1):
			for vertices_comb in combinations(vertices, i):
				self.verticesweight[frozenset(vertices_comb)] = sum(v.weight for v in vertices_comb)

		# print([x for x in self.verticesweight.items()])

	def hcost(self, state, action):
		if action == 'pass':
			return self.verticesweight[state.land]
		elif action == 'launch':
			return self.verticesweight[state.land]
		else:
			return self.verticesweight[state.land]
