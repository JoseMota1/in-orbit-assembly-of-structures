def cost_search(problem)

	node=Node();
	PATH_COST = 0;
	explored=[];
	frontier=Frontier() #a priority queue ordered by PATH-COST, with node as the only elemen

	while True:
		if not frontier:
			return failure

		node = heapq.heappop(frontier)	# chooses the lowest-cost node in frontier (first)
		if problem.goal(node.state):
			return problem.solution(node)

		explored.append(node.state);

		for action in problem.actions(node.state):
			child = problem.childnode(node, action)
			# TODO lower code is done in the Frontier class
			if child.state in explored  or (child.state in frontier and child.path_cost < node.cost):
				frontier.insert(child)
			elif child.state in frontier and child.cost > node.cost): # if coiso in ...
				frontier = child;
