# lista imutavel com acesso hash , lista duplamente ligada e dicionario ordenado
from collections import OrderedDict
from itertools import combinations, islice
from copy import copy
from heapq import heappush, heappop
from math import ceil
from time import perf_counter


class Frontier:
	""" Frontier class is initialized with an initial Node.
	It contains a priority queue and a dictionary.
	The dictionary contains the expanded nodes as keys, and
	as value the cost of each, and if it has been visited.
	To not go through the entire queue everytime a node is already
	expanded it is compared with the expanded dict, and verified if the
	cost is lower. If so, the cost its updated in the dict, and added to the
	queue.
	When a node is removed from the queue, it verifies in the dict
	if it had been removed before. If so, the value is discarded.
	"""
	def __init__(self, node):
		self.queue = list()
		self.expanded = dict()
		self.insert(node)

	def insert(self, node):
		if not self.expanded.get(node.state, False):
			heappush(self.queue, node)
			self.expanded[node.state] = [node.pathcost, False]
		elif node.pathcost < self.expanded[node.state][0]:
			heappush(self.queue, node)
			self.expanded[node.state][0] = node.pathcost

	def pop(self):
		while self.queue:
			node = heappop(self.queue)
			if not self.expanded[node.state][1]:
				self.expanded[node.state] = [node.pathcost, True]
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
			', f	ixed_cost: ' + str(self.fixed_cost) +
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

	def __eq__(self, other):
		return self.__slots__ == other.__slots__

	def __hash__(self):
		prime = 13
		result = 1
		result = result*prime + self.land.__hash__()
		result = result*prime + self.air.__hash__()
		result = result*prime + int(self.date)
		return result


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

		# used for the minweight and sumweight functions
		self.vertices_set = frozenset(self.vertices.keys())
		self.minweights = self.minweight()		# used in the action function

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

		self.sumweights = self.sumweight()

		# print([x for x in self.verticesweight.items()])

	def hcost(self, state, action):
		if not state.date and not state.land:
			return 0
		elif not state.date:
			return float('inf')

		launches = ( (l.date, l.max_payload, l.fixed_cost, l.variable_cost)
			for (key, l) in self.launches.items()
			if l.next_launch and (l.next_launch >= state.date)
			or not l.next_launch )

		nvertices = len(state.land)
		weightleft = self.sumweights[state.land]
		min_launches = 0

		maxpay = list()
		fcost = list()
		ucost = list()
		for l in launches:
			d, mp, f, v = l
			maxpay.append(mp)
			fcost.append(f)
			ucost.append((d, v))

		for mp in sorted(maxpay, reverse=True):
			if weightleft > 0:
				weightleft -= mp
				min_launches += 1
			else:
				min_launches += 1
				break

		if weightleft > 0:
			return float('inf')

		ucost.sort(key = lambda x: x[1])
		idx = 0
		full = [False] * len(ucost)
		wloaded = [0] * len(ucost)
		sumucost = 0
		w = 0
		for v in sorted(state.land, key = lambda x: self.vertices[x], reverse=True):
			w = self.vertices[v]
			if not full[idx] and self.launches[ucost[idx][0]].max_payload > (wloaded[idx] + w):
				wloaded[idx] += w
			else:
				if self.launches[ucost[idx][0]].max_payload == (wloaded[idx] + w):
					full[idx] = True
				while not full[idx] and self.launches[ucost[idx][0]].max_payload > (wloaded[idx] + w):
				idx += 1
				wloaded[idx] = w

		sumucost = sum(ucost[i][1] * wloaded[i] for i in range(len(ucost)))

		return sum(sorted(fcost)[:min_launches]) + sumucost
		"""
		varmin = min((self.launches[a].variable_cost for a in self.launches.keys() if self.launches[a].next_launch and (self.launches[a].next_launch >= state.date)), default = 0)
		fixmin = min((self.launches[a].fixed_cost for a in self.launches.keys() if self.launches[a].next_launch and (self.launches[a].next_launch >= state.date)), default = 0)
		maxpay = max((self.launches[a].max_payload for a in self.launches.keys() if self.launches[a].next_launch and (self.launches[a].next_launch >= state.date)), default = 1)
		costheuristic = ((fixmin/maxpay)+(varmin))*self.sumweights[pstate.land]

		return costheuristic
		"""
