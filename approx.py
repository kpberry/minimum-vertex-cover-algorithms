from datetime import datetime, timedelta
from random import seed, choice

from graph_utils import read_graph, copy_graph, remove_vertices, remove_isolates
from vc import construct_vc


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    return greedy_vc(graph, filename, cutoff_time)


def vertex_quality_getter(graph):
    def vertex_quality(x):
        return len(graph[x]) / min([len(graph[i]) for i in graph[x]])

    return vertex_quality


def random_vc(graph):
    seed(0)
    vc = [0] * (max(graph) + 1)
    while len(graph) > 0:
        u = choice(list(graph.keys()))
        v = choice(list(graph[u]))
        graph = remove_isolates(remove_vertices(graph, (u, v)))
        vc[u] = vc[v] = 1
    return vc


def greedy_vc(graph, filename=None, cutoff_time=None):
    graph = copy_graph(graph)
    start_time = cur_time = datetime.now()
    fast = construct_vc(graph)
    rand = construct_vc(graph)
    vc = [0] * (max(graph) + 1)
    base = None
    if filename is not None:
        base = filename.split('/')[-1].split('.')[0] \
               + '_Approx_' + str(cutoff_time)

    while cutoff_time is None or \
                    (cur_time - start_time) < timedelta(seconds=cutoff_time):
        num_vertices = len(graph)
        if num_vertices == 0:
            break
        best = max(list(graph.keys()), key=vertex_quality_getter(graph))
        vc[best] = 1
        for i in graph[best]:
            graph[i].remove(best)
            if len(graph[i]) == 0:
                del graph[i]
        del graph[best]
        cur_time = datetime.now()

    vc = min([vc, fast, rand], key=lambda x: sum(x))

    if base is not None:
        with open(base + '.trace', 'w') as trace:
            trace.write('{:0.2f}'.format(
                (cur_time - start_time).total_seconds()
            ))
            trace.write(',' + str(sum(vc)) + '\n')
        with open(base + '.sol', 'w') as sol:
            sol.write(str(sum(vc)) + '\n')
            sol.write(
                ','.join([str(i + 1) for i in range(len(vc)) if
                          vc[i] == 1]))

    return vc
