from datetime import datetime, timedelta
from random import random, seed

from graph_utils import read_graph


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    greedy_vc(graph, filename, cutoff_time, random_seed)


def greedy_vc(graph, filename, cutoff_time, random_seed):
    seed(random_seed)
    start_time = cur_time = datetime.now()
    vc = [0] * (max(graph) + 1)
    base = filename.split('/')[-1].split('.')[0] \
           + '_Approx_' + str(cutoff_time) + '_' \
           + str(random_seed)
    print(base)

    while (cur_time - start_time) < timedelta(seconds=cutoff_time):
        num_vertices = len(graph)
        if num_vertices == 0:
            break
        best = max(list(graph.keys()),
                   key=lambda x: len(graph[x]) * random() * 2)
        vc[best] = 1
        for i in graph[best]:
            graph[i].remove(best)
            if len(graph[i]) == 0:
                del graph[i]
        del graph[best]
        cur_time = datetime.now()

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
