from itertools import permutations
import csv
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def genPaths(nodes):   # generate all permutations of nodes regardless of connectivity 
    allPaths = permutations(nodes)
    paths = []
    for path in allPaths: paths.append(list(path))
    return paths


def checkPaths(graph, rem, path):
    if not rem:   # no nodes left to visit
        if not path: return 1
        else: return 0
    
    if not path:    # no nodes left in path
        if not rem: return 1
        else: return 0
    
    if len(path) != len(rem): return 0
        # path and remaining nodes must be same length
            # path < rem - won't visit all nodes
            # path > rem - must visit at least one node twice
    
    curr = path[0]
    nextSteps = path[1:]
    rem.remove(curr)   # remove node from list to visit
    
    if not nextSteps:
        if not rem: return 1    # path complete and no nodes left to visit, success
        else: return 0  # path complete but nodes left to visit
    
    if not rem:
        if not nextSteps: return 1
        else: return 0
    
    if (nextSteps[0] not in graph[curr]) or (nextSteps[0] not in rem): return 0
        # cannot get to next node in path from current node or next node already visited, bad path
    
    return checkPaths(graph, rem, nextSteps)    # recursively check path


def plotter(data) :
    maxX = list(sorted(data.keys()))
    maxVals = {}
    maxY = []
    for x in data.keys():
        for tup in data[x]:
            y = tup[0]
            try:
                if y > maxVals[x]: maxVals[x] = y   # keep track of highest value per number of nodes
            except KeyError:
                maxVals[x] = y

        for tup in data[x]:
            y = tup[0]
            if tup[1] == 'h': plt.scatter(x, y, color='green', s=5)
            else: plt.scatter(x, y, color='red', s=5)
    for x in maxX: maxY.append(maxVals[x])  # create list of max y values
    plt.plot(maxX, maxY, color='blue', linewidth=1)
    plt.xlabel("Number of Nodes")
    plt.ylabel("Time (in seconds)")
    plt.title("Time to Determine Hamiltonian Path Existence")
    ham = mpatches.Patch(color='green', label='Hamiltonian')
    nonHam = mpatches.Patch(color='red', label='Non-Hamiltonian')
    plt.legend(handles=[ham, nonHam])
    plt.savefig("plotHamiltonianPath_hflick.png")


def main(arguments=sys.argv[1:]):
    graph = {}
    control = 0
    v = 0
    e = 0
    pathsHolder = {}
    solveTimes = {}
    try:
        fileName = arguments[0]
    except IndexError:
        fileName = "dataCheckHamiltonianPath_hflick.cnf"
    try:
        with open(fileName, mode ='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                if not lines: pass
                elif lines[0] == 'c':     # reset graph dict on new graph
                    pass
                elif lines[0] == 'p':   # get number of vertices and edges
                    v = int(lines[2])
                    e = int(lines[3])
                    if not v in solveTimes: solveTimes[v] = []  # initialize for plotting
                elif lines[0] == 'v':   # add verticies to dict
                    for i in range(1, v+1): graph[int(lines[i])] = []
                    control = 1
                elif lines[0] == 'e':
                    graph[int(lines[1])].append(int(lines[2]))
                    graph[int(lines[2])].append(int(lines[1]))
                    e -= 1      # keep track of edges remaining
                if (e == 0) and (control):      # no edges left and all vertices read
                    nodes = list(graph.keys())
                    SAT = 'u'
                    goodPath = []
                    if v not in pathsHolder: pathsHolder[v] = genPaths(nodes)
                    # generate all permutations of nodes
                    #   save for future use to make program efficient especially for larger graphs
                    
                    start = time.time()
                    for path in pathsHolder[v]:  # check paths one at a time
                        remaining = nodes[:]    # copy list of nodes
                        result = checkPaths(graph, remaining, path)
                        if result:
                            SAT = 'h'
                            goodPath = path
                            break

                    end = time.time()
                    elapsed = end - start
                    if SAT == 'h':
                        print(f"Graph {graph} has a Hamiltonian path:\n\t{goodPath}")
                    else:
                        print(f"Graph {graph} does not have a Hamiltonian path")
                    solveTimes[v].append((elapsed, SAT))    # record time to solve and if hamiltonian
                    graph = {}  # reset graph for next problem
                    control = 0
                    
    except FileNotFoundError:
        print(f"File not found: {fileName}")
        return -1

    plotter(solveTimes)
    print("\nTimes to find a Hamiltonian path and existence of path, organized by number of nodes:")
    print(solveTimes)


if __name__ == '__main__':
    main()