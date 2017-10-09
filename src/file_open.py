tests_path = '../test/'

with open(tests_path + 'example.txt') as fd:
	lines = [line.strip().split(' ') for line in fd]
	
for x in lines:
	print(x)