# File containing auxiliary approximation algorithms, including a networkx
# implementation of edge deletion, maximum degree greedy selection, and
# greedy independent cover selection.
# Assumes that data is located in the folder ./Data/
# Will not be used by main.py
from datetime import datetime
from random import randint, seed

import networkx as nx


def read_graph(filename):
    G = nx.Graph()
    with open(filename, "r") as inputfile:
        graph_data = inputfile.readline()
        i = 0
        for line in inputfile:
            i += 1
            node_data = list(map(lambda x: int(x), line.split()))
            for node in node_data:
                G.add_edge(i, node)
    return G


# Approximation algorithm which iteratively selects edges, adds the
# endpoints to the vertex cover, then deletes the edge.
def edge_deletion(G):
    seed(0)
    c = []
    while nx.number_of_edges(G) != 0:
        edgesNum = nx.number_of_edges(G)
        rN = randint(0, edgesNum - 1)
        edges = list(G.edges())
        e = edges[rN]
        v1 = e[0]
        v2 = e[1]
        c.append(v1)
        c.append(v2)
        G.remove_node(v1)
        G.remove_node(v2)
    return c


# Approximation algorithm that greedily selects the vertex of max degree in
# the graph, then adds it and deletes any of its outgoing edges.
def maximum_degree_greedy(G):
    c = []
    while nx.number_of_edges(G) != 0:
        v = max(G.nodes, key=G.degree)
        c.append(v)
        G.remove_node(v)
    return c


# Approximation algorithm that greedily selects the vertex of min degree,
# adds each of its neighbors to the vertex cover, then deletes the newly
# covered edges.
def greedy_independent_cover(G):
    c = []
    while nx.number_of_edges(G) != 0:
        v = min(G.nodes, key=G.degree)
        v_list = list(G.neighbors(v))
        c.extend(v_list)
        G.remove_node(v)
        G.remove_nodes_from(v_list)
    return c

# Run the algorithm on an input graph with a specified time and faux random seed
def run(filename, cutoff_time, random_seed, algo='Approx2'):
    seed(random_seed)
    graph = read_graph(filename)

    start_time = datetime.now()
    vc = []
    if algo == 'Approx2':
        vc = edge_deletion(graph)
    elif algo == 'Approx3':
        vc = maximum_degree_greedy(graph)
    elif algo == 'Approx4':
        vc = greedy_independent_cover(graph)
    else:
        print('Invalid algorithm entered.')
    cur_time = datetime.now()

    print(len(vc))
    base = filename.split('/')[-1].split('.')[0] + '_' + algo + '_' + str(
        cutoff_time)
    with open(base + '.trace', 'w') as trace:
        trace.write('{:0.2f}'.format((cur_time - start_time).total_seconds()))
        trace.write(',' + str(len(vc)) + '\n')
    with open(base + '.sol', 'w') as sol:
        sol.write(str(len(vc)) + '\n')
        sol.write(','.join(sorted([str(v) for v in vc])))

if __name__ == '__main__':
    run('./data/Data/power.graph', 100000000, 0, algo='Approx4')