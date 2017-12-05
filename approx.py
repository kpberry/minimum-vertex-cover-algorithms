# File for the approximation algorithms used by main.py
# Contains an implementation of the MG algorithm, as described in the report,
# which greedily chooses vertices for a vertex cover using a scoring function.
# The scoring function we have chosen to use is the one returned by
# vertex_quality_getter, and scores a vertex by its number of neighbors
# vs. the fewest neighbors any of its neighbors has.

from datetime import datetime, timedelta
from random import seed

from graph_utils import read_graph, copy_graph


# Retrieves a function which will be used to measure vertex quality.
# This has been implemented this way to make its use as a key function for
# finding a max value in a graph possible.
def vertex_quality_getter(graph):
    def vertex_quality(x):
        # degree(x) / min(degree(neighbor)) for all neighbors of x
        return len(graph[x]) / min([len(graph[i]) for i in graph[x]])

    return vertex_quality


# Returns a VC via the edge deletion approximation algorithm.
def edge_deletion(graph):
    # Start with an empty vc (no vertices added)
    vc = [0] * (max(graph) + 1)
    for u in graph:
        # only add an edge if neither endpoint is already in the vc
        if not vc[u]:
            for v in graph[u]:
                if not vc[v]:
                    # add both vertices of an edge, then move onto a new vertex
                    vc[u] = vc[v] = 1
                    break
    return vc


def greedy_vc(graph, filename=None, cutoff_time=None):
    # basic setup
    graph = copy_graph(graph)
    start_time = cur_time = datetime.now()
    vc = [0] * (max(graph) + 1)

    # Loop while the graph has uncovered edges
    while len(graph) > 0 and cur_time - start_time < timedelta(
            seconds=cutoff_time):
        # get the best vertex and add it to the VC
        best = max(list(graph.keys()), key=vertex_quality_getter(graph))
        vc[best] = 1
        # remove the edges of the best vertex
        for i in graph[best]:
            graph[i].remove(best)
            if len(graph[i]) == 0:
                del graph[i]
        del graph[best]
        cur_time = datetime.now()

    # write the found solution
    base = filename.split('/')[-1].split('.')[0] + '_Approx_' + str(cutoff_time)
    with open(base + '.trace', 'w') as trace:
        trace.write('{:0.2f}'.format((cur_time - start_time).total_seconds()))
        trace.write(',' + str(sum(vc)) + '\n')
    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(vc)) + '\n')
        sol.write(','.join([str(i + 1) for i in range(len(vc)) if vc[i] == 1]))

    return vc


# Run the algorithm on an input graph with a specified time and faux random seed
def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    return greedy_vc(graph, filename, cutoff_time)
