# lista imutavel com acesso hash , lista duplamente ligada e dicionario ordenado
from collections import OrderedDict
from itertools import combinations, islice
from copy import copy
from heapq import heappush, heappop
from time import perf_counter

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
	__slots__ = ('land', 'air', 'date')

	def __init__(self, land, air, date):
		self.land = land
		self.air = air
		self.date = date

	def __repr__(self):
		return ('State LAND ' + str(self.land) +
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

		self.branchingfactor = []
		self.nexpandednodes = 0

		self.vertices_set = frozenset(self.vertices.keys())

		self.minweights = self.minweight()

	def initialnode(self):
		date = next(islice(self.launches, 1))
		state = State(frozenset(self.vertices.keys()), frozenset(), str(date))
		parent = False
		action = False
		pathcost = 0
		if self.HEURISTIC:
			cost = pathcost + self.hcost(state, action)
		else:
			cost = pathcost

		return Node(state, parent, action, pathcost, cost)

	def goal(self, state):
		if not state.land:
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

		actions.append('pass')

		minvw = self.minweights[state.land]
		maxv = int(max_payload/minvw)

		[actions.append(set(vertices)) for n in range(1, maxv + 1) for vertices in combinations(state.land, n)
			if sum(self.vertices[v] for v in vertices) <= max_payload
			if not state.air and len(vertices) == 1
			or not state.air
			and all( any(edge in vertices for edge in self.edges[v]) for v in vertices )
			or all( True if any(edge in state.air for edge in self.edges[v]) else any(edgeofedge in state.air for edge in self.edges[v] for edgeofedge in self.edges[edge] if edge in vertices)
			for v in vertices) ]
			#any(edge in state.air for edge in edges[v]) if edges[v] in vertices else edges[v] in state.ai
		# print(actions)
		self.branchingfactor.append(len(actions))
		return actions

	def childnode(self, parent, action):
		pstate = parent.state

		if action == 'pass':
			date = self.launches[pstate.date].next_launch
			state = State(frozenset(pstate.land), frozenset(pstate.air), date)
			pathcost = parent.pathcost
			if self.HEURISTIC:
				cost = pathcost + self.hcost(state, action)
			else:
				cost = pathcost

		else: # action Load vertices and Launch
			land = frozenset(v for v in list(pstate.land) if v not in action)
			loaded = frozenset(v for v in list(pstate.land) if v in action)
			air = pstate.air | loaded
			date = self.launches[pstate.date].next_launch
			state = State(land, air, date)
			pathcost = parent.pathcost + (
					self.launches[pstate.date].variable_cost *
					sum(self.vertices[v] for v in loaded) +
					self.launches[pstate.date].fixed_cost)
			if self.HEURISTIC:
				cost = pathcost + self.hcost(state, action)
			else:
				cost = pathcost

		return Node(state, parent, action, pathcost, cost)

	def sumweight(self):
		verticesweight = dict()
		for i in range(len(self.vertices_set)+1):
			for vertices_comb in combinations(self.vertices_set, i):
				verticesweight[frozenset(vertices_comb)] = sum(self.vertices[v] for v in vertices_comb)

		return verticesweight

	def minweight(self):
		verticesweight = dict()
		for i in range(len(self.vertices_set)+1):
			for vertices_comb in combinations(self.vertices_set, i):
				verticesweight[frozenset(vertices_comb)] = min((self.vertices[v] for v in vertices_comb), default = 0)

		return verticesweight

	def heuristics(self):
		self.HEURISTIC = True

		self.sumweights = sumweight()

		# print([x for x in self.verticesweight.items()])

	def hcost(self, state, action):
		if action == 'pass':
			return self.verticesweight[state.land]
		else:
			return self.verticesweight[state.land]
