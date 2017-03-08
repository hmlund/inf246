import random


def getPercentageMultiedges(edge_list):
    nmbr_of_multiedges = get_number_of_multiedges(edge_list)
    return (nmbr_of_multiedges/(len(edge_list))*100),nmbr_of_multiedges


def getPercentageSelfLoops(edge_list):
    numbr_of_loops = get_number_of_loops(edge_list)
    return (numbr_of_loops/(len(edge_list))*100),numbr_of_loops


def main():
    # Write a computer code to generate networks of size N with a power-law degree distribution with degree exponent
    # γ. Refer to SECTION 4.9 for the procedure. Generate three networks with γ = 2.2 and with N = 10^3, N = 10^4 and N
    #  = 10^5 nodes, respectively. What is the percentage of multi-link and selfloops in each network? Generate more
    # networks to plot this percentage in function of N. Do the same for networks with γ = 3.

    N = range(1000,600000,50000)
    Y = [2.2,3]

    print('{},{},{},{},{},{},{}'.format('N', 'Y', 'self_loops', 'multi_edge','#selfloops','#multiedges', '#Edges'))
    for y in Y:
        for n in N:

            # Creates the degree sequence
            degree_sequence = generate_degree_sequence(n, y)

            # Runs the conf-model and return the graphs as an edgelist representation
            edge_list = configuration_model(degree_sequence)

            percentageMultiedges,multi = getPercentageMultiedges(edge_list)
            percentageSelfLoops,self = getPercentageSelfLoops(edge_list)

            print('{},{},{},{},{},{},{}'.format(n,y,percentageSelfLoops,percentageMultiedges,self,multi,len(edge_list)))


def configuration_model(degree_sequence):
    # Randomly select a stub pair and connect them. Then randomly choose another pair from the remaining 2L - 2 stubs
    #  and connect them. This procedure is repeated until all stubs are paired up. Depending on the order in which
    # the stubs were chosen, we obtain different networks.
    # Must do something about 0 edges, but right now i only increase all edges with one so 0 = 1

    number_of_stubs = sum(degree_sequence)

    # Maps which stubs that belong to the different nodes
    stub_to_node_id = {}
    current = 0
    for i in range(len(degree_sequence)):
        degree = degree_sequence[i]
        for v in range(current, current + degree):
            stub_to_node_id[v] = i
        current = current + degree

    # Randomly selects two stubs that is then connected together
    # The two stubs are mapped to the correct node id, and included as an edge
    edges = []

    stubs = list(range(number_of_stubs))
    # Using shuffle that implements the  Fisher–Yates algorithm to give us an random ordering of the stubs.
    random.shuffle(stubs)

    # Selects two and two stubs that forms an edge
    for i in range(0, number_of_stubs, 2):
        stub_one = stubs[i]
        stub_two = stubs[i + 1]
        edges.append([stub_to_node_id[stub_one], stub_to_node_id[stub_two]])

    return edges




def generate_degree_sequence(n, y):
    # Generates normalized pk for each k
    # Calculates C
    C = 0
    for i in range(1, 100000):
        C += pow(i, -y)

    pk = []
    for j in range(1, n + 1):
        if (j > 1):
            pk.append((pow(j, -y) / C) + pk[j - 2])

        else:
            pk.append(pow(j, -y) / C)

    # The sum of the stublist must be even, we therefore repeat this process until that is the case.
    even = False
    stubList = []

    while (even != True):
        stubList = []
        # Generates a sequence of random numbers between 0,1
        random_numbers = []
        for i in range(n):
            random_numbers.append(random.random())

        # Creates a degree sequence by matching the random numbers with the percentage of pk
        for rn in random_numbers:
            i = 0
            k = 0
            while ((rn > pk[i]) and (i < n - 1)):
                k = i
                i += 1
            stubList.append(k + 1)

        # Check if even
        even = sum(stubList) % 2 == 0

    return stubList

# Finds all edges where i == j
def get_number_of_loops(edge_list):
    sum = 0
    for edge in edge_list:
        i, j = edge
        if (i == j):
            sum += 1
    return sum

# Finds all edges with the same two endpoints
def get_number_of_multiedges(edge_list):
    number_of_multiedges = 0
    dic = {}
    for edge in edge_list:
        e = str(sorted(edge))
        if(e in dic):
            number_of_multiedges += 1
        else:
            dic[e] = 1
    return number_of_multiedges

main()
