from math import log
from random import random

from graph_utils import get_edges


def crossover(a, b, graph, iterations=10):
    # TODO make this better
    # try to crossover randomly up to iterations times
    for i in range(iterations):
        index = int(random() * len(a))
        cur = a[:index] + b[index:]
        if is_solution(graph, cur):
            return cur
    # return the original vc if no crossover solution was found
    return a


def mutation(vc, graph, iterations=10, degree=None):
    # mutates the graph to try to find a similar solution
    # try flipping up to log_2 bits of the solution
    if degree is None:
        degree = log(len(vc)) / log(2)
    # try to flip bits up to iterations times, returning if a solution is found
    for i in range(iterations):
        gene_copy = [i for i in vc]
        for _ in range(int(random() * degree + 1)):
            gene_copy[int(random() * len(vc))] ^= 1
        if is_solution(graph, gene_copy):
            return gene_copy
    # return the original vc if no mutated solution was found
    return vc


def is_solution(graph, vc):
    for u in graph:
        for v in graph[u]:
            if vc[u] + vc[v] == 0:
                return False
    return True


def construct_vc(graph, return_losses=False):
    vc = [0] * (max(graph) + 1)
    edges = get_edges(graph)
    for u, v in edges:
        if vc[u] + vc[v] == 0:
            vc[max(u, v, key=lambda x: len(graph[x]))] = 1

    losses = [0] * len(vc)
    for u, v in edges:
        if vc[u] + vc[v] == 1:
            if vc[u] > vc[v]:
                losses[u] += 1
            else:
                losses[v] += 1

    for u in range(len(vc)):
        if losses[u] == 0:
            vc[u] = 0
            if u in graph:
                for v in graph[u]:
                    losses[v] += 1

    if return_losses:
        return vc, losses
    return vc


def eval_fitness(graph, vc):
    # get the total number of edges to cover vs. the number covered by vc
    covered_edges = 0
    num_edges = sum([len(graph[i]) for i in graph])
    marked = [False] * len(vc)
    for u in graph:
        if not marked[u]:
            for v in graph[u]:
                if not marked[v]:
                    if vc[u] + vc[v] > 0:
                        covered_edges += 1
                        marked[u] = True
                        marked[v] = True
    return covered_edges - sum(vc) + len(vc)
