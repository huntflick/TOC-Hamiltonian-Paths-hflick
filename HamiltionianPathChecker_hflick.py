from itertools import permutations
import csv
import time


def genPaths(nodes):   # generate all permutations of nodes regardless of connectivity 
    allPaths = permutations(nodes)
    paths = []
    for path in allPaths:
        paths.append(list(path))
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

def main():
    graph = {}
    v = 0
    e = 0

    solveTimes = {}
    file_name = "hamiltonian_path_test_cases2.cnf"
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if lines[0] == 'c':     # reset graph dict on new graph
                graph = {}
                control = 0
            elif lines[0] == 'p':   # get number of vertices and edges
                v = int(lines[2])
                e = int(lines[3])
                if not v in solveTimes:
                    solveTimes[v] = []
            elif lines[0] == 'v':   # add verticies to dict
                for i in range(1, v+1):
                    graph[int(lines[i])] = []
                control = 1
            elif lines[0] == 'e':
                graph[int(lines[1])].append(int(lines[2]))
                graph[int(lines[2])].append(int(lines[1]))
                e -= 1      # keep track of edges remaining
            if (e == 0) and (control):      # no edges left and all vertices read
                nodes = list(graph.keys())
                paths = []
                SAT = 'u'
                goodPath = []
                paths = genPaths(nodes)  # generate all permutations that could be a hamiltonian path
                
                start = time.time()
                for path in paths:  # check paths one at a time
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
                print(solveTimes)


if __name__ == '__main__':
    main()