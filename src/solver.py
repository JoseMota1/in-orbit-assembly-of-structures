import sys, getopt
import searchstrategies
from datastructures import *

def getinfo(lines):
    """ Retrieves the information present in the file given.

    Returns 3 dictionaries, each with information on the vertices, edges and
    launches respectively.
    """

    lines.sort(reverse=True) # Reverse alphabetic order, so the V comes 1st
    vertices = dict()
    edges = dict()
    launches = dict()

    for line in lines:
        if not line:
            continue
        if line[0][0] == 'V':
            name = line[0]
            value = line[1]
            vertices[name] = float(value)
        elif line[0] == 'E':
            v1 = line[1]
            v2 = line[2]
            edges.setdefault(v1, set()).add(v2)
            edges.setdefault(v2, set()).add(v1)
        elif line[0] == 'L':
            launches[line[1]] = Launch(line[1], float(line[2]), float(line[3]),
                float(line[4]), False)

    launches = OrderedDict(sorted(launches.items(),
                        key = lambda t: (t[0][4:]+t[0][2:4]+t[0][0:2]) ))
    previous_launch = False
    for (key, value) in reversed(launches.items()):
        value.next_launch = previous_launch
        previous_launch = key

    return (vertices, edges, launches)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:u:')
    except getopt.GetoptError:
        print("python solver.py -i 'filename.txt'")
        sys.exit(2)

    with open(opts[0][1]) as fd:
        lines = [line.strip().split() for line in fd]

    vertices, edges, launches = getinfo(lines)
    problem = Problem(vertices, edges, launches)

    for opt, arg in opts:
        if opt == '-i':
            problem.heuristics()
            start = perf_counter()
            (solution, cost) = searchstrategies.solve(problem)
            print('Time elapsed: ', perf_counter() - start)
        elif opt == '-u':
            start = perf_counter()
            (solution, cost) = searchstrategies.solve(problem)
            print('Time elapsed: ', perf_counter() - start)

    if not solution:
        print("No solution found!")
        sys.exit(0)

    date = next(islice(launches, 1))
    launch = []
    for x in solution:
        if not x == 'pass':
            launchcost = sum(vertices[v] for v in x) * launches[date].variable_cost + launches[date].fixed_cost
            print(launches[date].date, '  ', ' '.join(v for v in x), '  ', launchcost)
            date = launches[date].next_launch
        else: # pass
            date = launches[date].next_launch

    print('Cost = ', cost)


if __name__ == '__main__':
    main(sys.argv[1:])
