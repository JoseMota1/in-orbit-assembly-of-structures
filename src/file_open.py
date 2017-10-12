tests_path = '../test/'
from datastructures import *

with open(tests_path + 'example.txt') as fd:
	lines = [line.strip().split(' ') for line in fd]
	
lines.sort(reverse=True)
#print(lines)
vertices = {}
edges = deque()
launches = deque()

for line in lines:
	if line[0][0]=='V':
		id = line[0]
		value = line[1]
		vertices[id] = Vertice(id, value)
	elif line[0]=='E':
		v1 = line[1]
		v2 = line[2]
		edges.append( Edge( vertices[v1], vertices[v2]) )
	elif line[0]=='L':
		launches.append( Launch( line[1], line[2], line[3], line[4]) )
		
#print(vertices)
#print(edges)
#print(launches)