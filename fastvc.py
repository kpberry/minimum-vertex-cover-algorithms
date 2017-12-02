from datetime import datetime, timedelta
from random import choice, seed

from graph_utils import get_edges, read_graph
from vc import construct_vc, is_solution


def choose_rm_vertex(losses, vc, k=50):
    indices = [i for i in range(len(vc)) if vc[i] == 1]
    best = indices[0]
    for i in range(k):
        r = choice(indices)
        if losses[r] < losses[best]:
            best = r
    return best


def get_uncovered_edge(edges, vc):
    r = choice(edges)
    while vc[r[0]] + vc[r[1]] > 0:
        r = choice(edges)
    return r


def fast_vc(graph, filename, cutoff_time, random_seed):
    seed(random_seed)

    vc, losses = construct_vc(graph, return_losses=True)
    gains = [0] * len(vc)
    edges = get_edges(graph)
    best = None

    start_time = cur_time = datetime.now()
    inf = float('inf')
    base = filename.split('/')[-1].split('.')[0] \
           + '_LS2_' + str(cutoff_time) + '_' \
           + str(random_seed)
    with open(base + '.trace', 'w') as trace:
        while cur_time - start_time < timedelta(seconds=cutoff_time):
            if is_solution(graph, vc):
                print(sum(vc))
                best = [i for i in vc]
                min_loss = min([i for i in range(len(vc))],
                               key=lambda i: inf if vc[i] == 0 else losses[i])
                vc[min_loss] = 0
                gains[min_loss] = 0
                for v in graph[min_loss]:
                    if vc[v] == 0:
                        gains[v] += 1
                    else:
                        losses[v] += 1
                continue
            u = choose_rm_vertex(losses, vc)
            vc[u] = 0
            gains[u] = 0
            for v in graph[u]:
                if vc[v] == 0:
                    gains[v] += 1
                else:
                    losses[v] += 1
            e0, e1 = get_uncovered_edge(edges, vc)
            u = max(e0, e1, key=lambda x: gains[x])
            vc[u] = 1
            for v in graph[u]:
                if vc[v] == 0:
                    gains[v] -= 1
                else:
                    losses[v] -= 1
            cur_time = datetime.now()
            # log results
            trace.write('{:0.2f}'.format(
                (cur_time - start_time).total_seconds()
            ))
            trace.write(',' + str(sum(best)) + '\n')

    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(best)) + '\n')
        sol.write(
            ','.join([str(i + 1) for i in range(len(best)) if best[i] == 1]))
    return best


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    fast_vc(graph, filename, cutoff_time, random_seed)


if __name__ == '__main__':
    run('./data/Data/star.graph', 600, 0)
