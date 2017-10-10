tests_path = '../test/'
from datastructures import *

with open(tests_path + 'example.txt') as fd:
	lines = [line.strip().split(' ') for line in fd]
	
vertices = {}
edges = []
launches = []

for line in lines:
	if line[0][0]=='V':
		vertices[line[0][1:]] = line[1]
	elif line[0][0]=='E':
		edges.append( Edge( vertices[line[1][1:]], vertices[line[2][1:]] ) )
	elif line[0][0]=='L':
		launches.append( Launch( line[1], line[2], line[3], line[4]) )
	else:
		print(line)
		
print(vertices)
print(edges)
print(launches)