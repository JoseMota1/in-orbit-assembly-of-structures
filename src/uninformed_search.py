def cost_search(problem)

	node=a;
	PATH_COST = 0;
	explored=[];
	ordered_front=heapsort(frontier) #a priority queue ordered by PATH-COST, with node as the only elemen

	while (len(ordered_front) > 0)
		if len(frontier) == 0
			return failure

		node = heapq.heappop(frontier)	# chooses the lowest-cost node in frontier (first)

		if problem.GOAL_TEST(node.STATE) 
			explored.append(node.STATE);
		
		for each_action in problem.ACTIONS(node.STATE)
			child = CHILD_NODE(problem, node, action);
			if (present_state(explored,child)  || present_state(frontier, child)) && (child.path_cost < node.path_cost)
				frontier.append(child);
			elif present_state(frontier,child) && child.path_cost > node.path_cost)
				frontier = child;
	return result
	

def present_state(lista,node)
i=0;
	while i<= len(lista)
		if lista[i] == node.STATE;
			return 1;
			break
		else
			return 0;
	i=i+1;
			
		
def CHILD_NODE(problem, parent , action) 

	node.STATE = RESULT(parent.STATE, action),
	node.PARENT = parent
	ACTION = action
	node.PATH_COST = parent.PATH_COST + problem.STEP_COST(parent.STATE, action)
return node