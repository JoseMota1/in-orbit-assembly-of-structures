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
			self.expanded[node.state] = [node.cost, False]
		elif node.cost < self.expanded[node.state][0]:
			print('Replace')
			heappush(self.queue, node)
			self.expanded[node.state][0] = node.cost

	def pop(self):
		while True:
			node = heappop(self.queue)
			if not self.expanded[node.state][1]:
				self.expanded[node.state] = [node.cost, True]
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
		return ('State land: ' + str(self.land) +
			' loaded ' + str(self.loaded) +
			' air ' + str(self.air) +
			' date ' + str(self.date))


class Node:
	__slots__ = ('state', 'parent', 'action', 'cost')

	def __init__(self, state, parent, action, cost):
		self.state = state
		self.parent = parent
		self.action = action
		self.cost = cost

	def __repr__(self):
		return ('Node state: ' + str(self.state) +
			' from Parent ' + str(self.parent) +
			' with action: ' + str(self.action) +
			' and cost ' + str(self.cost))

	def __lt__(self, other):
		return self.cost < other.cost


class Problem:

	def __init__(self, vertices, edges, launches):
		self.vertices = vertices
		self.edges = edges
		self.launches = launches

	def initialstate(self):
		initialdate = next(islice(self.launches, 1))
		return State(list(self.vertices.values()), [], [], str(initialdate))

	def goal(self, state):
		if not state.land and not state.loaded:
			return True
		return False

	def actions(self, state):
		actions = []

		# We are assuming that the launch date is an unique id
		launch = self.launches.get(state.date, 0)
		if launch:
			max_payload = launch.max_payload
		else:
			#print('actions@False: ', actions)
			return actions

		if not state.loaded:
			actions.append('pass')
		elif ( (len(state.loaded) > 1) or
				(len(state.loaded) == 1
					and any(edge in state.air for edge in self.edges[state.loaded[0]])) or
				(len(state.loaded) == 1 and not state.air) ):
			actions.append('launch')
		[actions.append(vertice) for vertice in state.land
			if sum(vertice.weight for vertice in state.loaded) + vertice.weight < max_payload]
		# if any(self.edges[vertice]) in self.state.air + self.state.loaded or not self.state.air]

		#print('max_payload', max_payload, ' actions@True: ', actions)
		return actions

	def childnode(self, parent, action):
		start = perf_counter()
		state = deepcopy(parent.state)
		t1 = perf_counter()
		if action == 'pass':
			state.date = self.launches[state.date].next_launch
			cost = parent.cost
		elif action == 'launch':
			state.air = state.air + state.loaded
			state.loaded = []
			cost = parent.cost + self.launches[state.date].fixed_cost
			state.date = self.launches[state.date].next_launch
		else:
			state.land.remove(action)
			state.loaded.append(action)
			cost = parent.cost + (
				self.launches[state.date].variable_cost *
				self.vertices[action.name].weight)

		t2 = perf_counter()
		n = Node(state, parent, action, cost)
		t3 = perf_counter()

		p_deepcopy = 100*(t1 - start)/(t3 - start)
		p_actions = 100*(t2 - t1)/(t3 - start)
		p_node = 100*(t3 - t2)/(t3 - start)

		return n, p_deepcopy, p_actions, p_node
