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
        if not path:
            return 1
        else:
            return 0
    
    if not path:    # no nodes left in path
        if not rem:
            return 1
        else:
            return 0
    
    if len(path) != len(rem):
        # path and remaining nodes must be same length
            # path < rem - won't visit all nodes
            # path > rem - must visit at least one node twice
        return 0
    
    curr = path[0]
    nextSteps = path[1:]
    rem.remove(curr)   # remove node from list to visit
    
    if not nextSteps:
        if not rem:     # path complete and no nodes left to visit, success
            return 1
        else:   # path complete but nodes left to visit
            return 0
    
    if not rem:
        if not nextSteps:
            return 1
        else:
            return 0
    
    if (nextSteps[0] not in graph[curr]) or (nextSteps[0] not in rem):
        # cannot get to next node in path from current node or next node already visited, bad path
        return 0
    
    return checkPaths(graph, rem, nextSteps)    # recursively check path

def main():
    graph = {}
    v = 0
    e = 0
    goodTime = 0
    maxGoodTime = 0
    badTime = 0
    maxBadTime = 0

    solveTimes = []
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
            elif lines[0] == 'v':   # add verticies to dict
                for i in range(1, v+1):
                    graph[int(lines[i])] = []
                control = 1
            elif lines[0] == 'e':
                graph[int(lines[1])].append(int(lines[2]))
                graph[int(lines[2])].append(int(lines[1]))
                e -= 1      # keep track of edges remaining
            if (e == 0) and (control):
                nodes = list(graph.keys())
                paths = []
                good = 0
                bad = 0
                graphTime = 0
                # goodTime = 0
                # maxGoodTime = 0
                # bad = 0
                # badTime = 0
                # maxBadTime = 0
                paths = genPaths(nodes)  # generate all permutations that could be a hamiltonian path
                
                for path in paths:  # check paths one at a time
                    remaining = nodes[:]    # copy list of nodes
                    start = time.time()
                    result = checkPaths(graph, remaining, path)
                    end = time.time()
                    elapsed = end - start

                    if result:
                        good = 1
                        graphTime += elapsed
                        if maxGoodTime < elapsed:
                            maxGoodTime = elapsed
                        break

                if good == 1:
                    print(f"Graph {graph} has a Hamiltonian path")
                else:
                    print(f"Graph {graph} does not have a Hamiltonian path")



if __name__ == '__main__':
    main()