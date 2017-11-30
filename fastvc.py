from datetime import datetime, timedelta
from random import choice

from graph_utils import get_edges
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


def fast_vc(graph):
    print('finding fastvc...')
    vc, losses = construct_vc(graph, return_losses=True)
    gains = [0] * len(vc)
    edges = get_edges(graph)
    best = None

    t0 = datetime.now()
    inf = float('inf')
    while datetime.now() - t0 < timedelta(seconds=1):
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
    print('Fast vc found')
    return best
