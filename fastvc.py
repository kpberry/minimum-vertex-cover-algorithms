# File containing an implementation of the FastVC algorithm.
# No modifications have been made to the original algorithm, except ties are
# broken arbitrarily instead of in favor of the older vertex.

from datetime import datetime, timedelta
from random import choice, seed

from graph_utils import get_edges, read_graph
from vc import is_solution


# Choose a vertex to remove based on its loss value
def choose_rm_vertex(losses, vc, k=50):
    # Get all of the vertices which are currently in the VC
    indices = [i for i in range(len(vc)) if vc[i] == 1]
    best = indices[0]
    # Try 50 different candidates and choose the one with the best loss
    for i in range(k):
        r = choice(indices)
        if losses[r] < losses[best]:
            best = r
    return best


def get_uncovered_edge(edges, vc):
    # Keep getting random edges until one is uncovered, then return that one
    r = choice(edges)
    while vc[r[0]] + vc[r[1]] > 0:
        r = choice(edges)
    return r


def construct_vc(graph, return_losses=False):
    # Keep adding the more connected vertex from edges in the graph until
    # all edges have been covered, essentially
    vc = [0] * (max(graph) + 1)
    edges = get_edges(graph)
    for u, v in edges:
        if vc[u] + vc[v] == 0:
            vc[max(u, v, key=lambda x: len(graph[x]))] = 1

    # Compute the loss for each vertex in the graph
    losses = [0] * len(vc)
    for u, v in edges:
        # Increment the loss on the side of the edge with the vertex in the VC
        if vc[u] + vc[v] == 1:
            if vc[u] > vc[v]:
                losses[u] += 1
            else:
                losses[v] += 1

    # Remove unnecessary vertices from the VC (those with loss 0)
    for u in range(len(vc)):
        if losses[u] == 0:
            vc[u] = 0
            if u in graph:
                for v in graph[u]:
                    losses[v] += 1

    # Return the VC and the losses, since the losses will be used by FastVC
    if return_losses:
        return vc, losses
    return vc


def fast_vc(graph, filename, cutoff_time, random_seed):
    seed(random_seed)

    # Basic setup
    vc, losses = construct_vc(graph, return_losses=True)
    gains = [0] * len(vc)
    edges = get_edges(graph)
    best = None

    # IO stuff
    start_time = cur_time = datetime.now()
    inf = float('inf')
    base = filename.split('/')[-1].split('.')[0] \
           + '_LS2_' + str(cutoff_time) + '_' \
           + str(random_seed)

    with open(base + '.trace', 'w') as trace:
        # Iterate until time runs out
        while cur_time - start_time < timedelta(seconds=cutoff_time):
            if is_solution(graph, vc):
                print(sum(vc))
                # Since vertices are only shuffled around when the candidate
                # is not a solution, any time the candidate is a solution, it
                # will be the best one
                best = [i for i in vc]

                # log results
                trace.write('{:0.2f}'.format(
                    (cur_time - start_time).total_seconds()
                ))
                trace.write(',' + str(sum(best)) + '\n')
                # Find the vertex with minimum loss and remove it
                min_loss = min([i for i in range(len(vc))],
                               key=lambda i: inf if vc[i] == 0 else losses[i])
                vc[min_loss] = 0
                # Gains is 0 now for the vertex because it is in the VCC
                gains[min_loss] = 0
                # Update the losses and gains of all neighbors to the min loss
                # vertex; they should all increase because edges will now
                # potentially be uncovered
                for v in graph[min_loss]:
                    if vc[v] == 0:
                        gains[v] += 1
                    else:
                        losses[v] += 1
                continue
            # choose the vertex with approximately minimum loss and remove it
            u = choose_rm_vertex(losses, vc)
            vc[u] = 0
            gains[u] = 0
            # update the losses and gains of surrounding vertices accordingly
            for v in graph[u]:
                if vc[v] == 0:
                    gains[v] += 1
                else:
                    losses[v] += 1
            # find a random uncovered edge and add its most connected endpoint
            # to the VC
            e0, e1 = get_uncovered_edge(edges, vc)
            u = max(e0, e1, key=lambda x: gains[x])
            vc[u] = 1
            # Update the losses and gains accordingly; they decrease because
            # more edges are covered now
            for v in graph[u]:
                if vc[v] == 0:
                    gains[v] -= 1
                else:
                    losses[v] -= 1
            cur_time = datetime.now()

    # IO stuff
    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(best)) + '\n')
        sol.write(
            ','.join([str(i + 1) for i in range(len(best)) if best[i] == 1]))
    return best


# Run the algorithm on an input graph with a specified time and random seed
def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    fast_vc(graph, filename, cutoff_time, random_seed)
