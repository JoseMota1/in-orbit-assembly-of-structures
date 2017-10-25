from datastructures import Frontier, Node, State, combinations

def solution(node):
	# print('Solutions')
	actions = []
	while node:
		actions.append(node.action)
		node = node.parent

	return reversed(actions[:-1])

def solve(problem, opt):

	node = Node(problem.initialstate(), False, False, 0)

	""" Frontier is a priority queue ordered by PATH-COST,
		with __node__ as the only element.
	"""
	frontier = Frontier(node)
	explored = set()

	while True:
		# print(frontier.queue)
		if not frontier.queue:
			return False

		node = frontier.pop() # Chooses the lowest-cost node in frontier (first)
		print('parent ', node)
		if problem.goal(node.state):
			return solution(node)

		explored.add(node.state)

		for action in problem.actions(node.state):
			child = problem.childnode(node, action, opt)
			if child.state in explored:
				continue

			print('child ', child)
			# TODO lower code is done in the Frontier class
			frontier.insert(child)
