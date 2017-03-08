import random

def toGephi(graph, N, k):
    with open('erdos-renyi-{}-{}-edges.txt'.format(N,k), 'w') as file:
        file.write('Source,Target\n')
        for i in graph:
            for j in graph[i]:
                file.write(str(i) + "," + str(j) + '\n')
    with open('erdos-renyi-{}-{}-nodes.txt'.format(N,k), 'w') as file:
        file.write('id\n')
        for i in range(500):
            file.write(str(i)+'\n')

def Main():
    # Start with N isolated nodes
    N = 500
    K = [0.8,1,8]

    for k in K:
        # Calculates p, given <k> = p(N-1)
        p = k / (N-1)
        graph = erdos_renyi_graph(N, p)

        toGephi(graph, N, k)


# Returns a list with all permutations/all all pairs
def get_all_pairs(N):
    allPairs = []

    for i in range(N):
        for j in range(i, N):
            if (i != j):
                allPairs.append([i, j])

    return allPairs


# Creates the graph and returns a adjacency list representation of the graph
def erdos_renyi_graph(N, p):
    graph = {}
    for i in range(N):
        graph[i] = []
    allNodePairs = get_all_pairs(N)

    for pair in allNodePairs:
        if random.random() <= p:
            x, y = pair
            graph[x].append(y)
            graph[y].append(x)


    return graph


Main()
