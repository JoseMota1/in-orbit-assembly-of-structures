from datastructures import Frontier, Node, State

def solution(node):
	actions = []
	while node:
		actions.append(node.action)
		node = node.parent
		# print(node)

	# print(actions)
	return reversed(actions)

def solve(problem):

	node = Node(problem.initialstate(), False, False, 0)
	""" Frontier is a priority queue ordered by PATH-COST,
		with __node__ as the only element.
	"""
	frontier = Frontier(node)
	explored = set()

	while True:
		if not frontier.queue:
			return False

		node = frontier.pop() # Chooses the lowest-cost node in frontier (first)
		if problem.goal(node.state):
			return solution(node)

		explored.add(node.state)

		for action in problem.actions(node.state):
			print(action)
			child = problem.childnode(node, action)

			print(node.state)
			print('\n')
			# TODO lower code is done in the Frontier class
			frontier.insert(child)
