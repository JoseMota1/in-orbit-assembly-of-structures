from datastructures import Frontier, Node, State, perf_counter

def solution(node):
	# print('Solutions')
	actions = []
	while node:
		actions.append(node.action)
		node = node.parent

	return reversed(actions[:-1])

def solve(problem):

	node = Node(problem.initialstate(), False, False, 0)
	""" Frontier is a priority queue ordered by PATH-COST,
		with __node__ as the only element.
	"""
	frontier = Frontier(node)
	explored = set()

	i = 0
	actions = 0
	actions_notexplored = 0
	t_pop = 0
	t_goal = 0
	t_add = 0
	t_child = 0
	t_in = 0
	t_insert = 0
	array_deepcopy = []
	array_actions = []
	array_node = []
	while True:
		# print(frontier.queue)
		if not frontier.queue:
			return False

		start = perf_counter()
		node = frontier.pop() # Chooses the lowest-cost node in frontier (first)
		t1 = perf_counter()
		t_pop = t_pop + (t1 - start)
		#print(node.state)
		if problem.goal(node.state):
			return solution(node)
		t2 = perf_counter()
		t_goal = t_goal + (t2 - t1)
		explored.add(node.state)
		t1 = perf_counter()
		t_add = t_add + (t1 - t2)

		#print('Parent ' + str(node.state))
		for action in problem.actions(node.state):
			start = perf_counter()
			child, p_deepcopy, p_actions, p_node, p_action = problem.childnode(node, action)
			t1 = perf_counter()
			t_child = t_child + (t1 - start)
			if child.state in explored:
				actions_notexplored = actions_notexplored + 1
				continue
			t2 = perf_counter()
			t_in = t_in + (t2 - t1)
			#print('Child ' + str(child.state))
			#print('\n')
			# TODO lower code is done in the Frontier class
			frontier.insert(child)
			t1 = perf_counter()
			t_insert = t_insert + (t1 - t2)
			array_deepcopy.append(p_deepcopy)
			array_actions.append(p_actions)
			array_node.append(p_node)
			#print(len(frontier.queue))
		if i > 10000:
			break
		i = i + 1

	print('Time to pop = ', t_pop)
	print('Time to test goal = ', t_goal)
	print('Time to add explored = ', t_add)
	print('Time to create child = ', t_child)
	print('Time to check if in explored = ', t_in)
	print('Time to insert = ', t_insert)
	print('Child already explored = ', actions_notexplored)

	print("% time in deepcopy = ", sum(array_deepcopy)/len(array_deepcopy))
	print("% time in actions = ", sum(array_actions)/len(array_actions))
	print("% time creating Node = ", sum(array_node)/len(array_node))
