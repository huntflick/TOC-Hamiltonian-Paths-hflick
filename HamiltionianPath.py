from itertools import permutations
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
        # path and remaininng nodes must be same length
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
    graph = {1 : [2, 3, 4],
             2 : [1, 3, 5],
             3 : [1, 2, 4],
             4 : [1, 3, 5],
             5 : [2, 4]
             }
    nodes = list(graph.keys())
    paths = []
    good = 0
    goodTime = 0
    maxGoodTime = 0
    bad = 0
    badTime = 0
    maxBadTime = 0
    paths = genPaths(nodes)  # generate all permutations that could be a hamiltonian path
    for path in paths:  # check paths one at a time
        remaining = nodes[:]    # copy list of nodes
        start = time.time()
        result = checkPaths(graph, remaining, path)
        end = time.time()
        elapsed = end - start

        if result:
            good += 1
            goodTime += elapsed
            if maxGoodTime < elapsed:
                maxGoodTime = elapsed
            print(f"{path} is a Hamiltonian path.")
        else:
            bad += 1
            badTime += elapsed
            if maxBadTime < elapsed:
                maxBadTime = elapsed
            print(f"{path} is not a Hamiltonian path.")
    if good == 1:
        if bad == 1:
            print(f"There is {good} Hamiltonian path and {bad} invalid or non-Hamiltonian path.")
        else:
            print(f"There is {good} Hamiltonian path and {bad} invalid or non-Hamiltonian paths.")         
    else:
        if bad == 1:
            print(f"There are {good} Hamiltonian paths and {bad} invalid or non-Hamiltonian path.")
        else:
            print(f"There are {good} Hamiltonian paths and {bad} invalid or non-Hamiltonian paths.")
    print(f"Max Hamiltonian time:           {maxGoodTime * 10**6} microseconds")
    print(f"Max non-Hamiltonian time:       {maxBadTime * 10**6} microseconds")
    print(f"Average Hamiltonian time:       {(goodTime/good) * 10**6} microseconds")
    print(f"Average non-Hamiltonian time:   {(badTime/bad) * 10**6} microseconds")



if __name__ == '__main__':
    main()