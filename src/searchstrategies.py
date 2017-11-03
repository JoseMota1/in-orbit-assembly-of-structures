from datastructures import Frontier, Node, State, combinations

nexpanded = 0

def solution(node):
	# print('Solutions')
	actions = []
	pathcost = node.pathcost
	while node:
		actions.append(node.action)
		node = node.parent

	global nexpanded
	return (reversed(actions[:-1]), pathcost, nexpanded)

def solve(problem):

	node = problem.initialnode()

	""" Frontier is a priority queue ordered by PATH-COST,
		with __node__ as the only element.
	"""
	frontier = Frontier(node)
	explored = set()

	global nexpanded
	while True:
		if not frontier.queue:
			return False

		node = frontier.pop() # Chooses the lowest-cost node in frontier
		#print('\nparent ', node)
		if problem.goal(node.state):
			return solution(node)

		explored.add(node.state)

		for action in problem.actions(node.state):
			child = problem.childnode(node, action)
			if child.state in explored:
				continue

			#print('child  ', child)
			frontier.insert(child)
			nexpanded += 1
