test_path = '../test/'
from datastructures import *

with open(test_path + 'example.txt') as fd:
	lines = [line.strip().split(' ') for line in fd]
	
lines.sort(reverse=True) #ordem alfabetica ao contrario V L E
#print(lines)
vertices = dict()
edges = dict()
launches = dict()

for line in lines:
	if line[0][0]=='V':
		id = line[0]
		value = line[1]
		vertices[id] = Vertice(id, float(value))
	elif line[0]=='E':
		v1 = vertices[line[1]]
		v2 = vertices[line[2]]
		edges.setdefault(v1, []).append(v2)
		edges.setdefault(v2, []).append(v1)
	elif line[0]=='L':
		launches[line[1]] = Launch(line[1], float(line[2]), float(line[3]), float(line[4]))

				
#print(vertices)
#print(edges)
d = OrderedDict(sorted(launches.items(), key=lambda t: (t[0][4:]+t[0][2:4]+t[0][0:2]) ))
print(d.keys())
for launch in launches:
	print(launch)
problem = Problem(vertices, edges, launches)

#print(list(vertices.values()))

state = State(list(vertices.values()), [], '28112017')

#print(problem.actions(state))
