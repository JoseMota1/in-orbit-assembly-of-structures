tests_path = '../test/'

with open(tests_path + 'example.txt') as fd:
	lines = [line.strip().split(' ') for line in fd]

for line in lines:
	if line[0][0]=='V':
		V_id = line[0]
		weight = line[1]
	elif line[0][0]=='E':
		V_id = line[0]
		Vid1 = line[1]
		Vid2 = line[2]
	elif line[0][0]=='L':
		date = line[1]
		max_payload = line[2]
		fixed_cost = line[3]
		variable_cost = line[4]
	else:
		print(line)

print(stop-start)