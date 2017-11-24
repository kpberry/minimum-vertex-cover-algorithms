from math import log
from random import random, seed, randint, choice
import networkx as nx
from datetime import datetime


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


def get_neighbors(vc, graph, iterations=10, degree=None):
    # same procedure as mutation, but adds all solutions to a list of results
    results = []
    if degree is None:
        degree = log(len(vc)) / log(2)
    while len(results) < iterations:
        gene_copy = [i for i in vc]
        for _ in range(int(random() * degree + 1)):
            gene_copy[int(random() * len(vc))] ^= 1
        if is_solution(graph, gene_copy):
            results.append(gene_copy)
    return results


def is_solution(graph, vc):
    # returns false if any edge does not have an endpoint in vc
    for v in graph:
        for u in graph[v]:
            if vc[v] + vc[u] == 0:
                return False
    return True


def gen_vc(graph):
    result = [0] * (max(graph) + 1)
    copy = {v: set([i for i in graph[v]]) for v in graph}
    for i in greedy_vc(copy):
        result[i] = 1
    return result


def greedy_vc(graph):
    t = datetime.now()
    c = []
    while True:
        num_vertices = len(graph)
        if num_vertices == 0:
            print(datetime.now() - t)
            print(len(c))
            return c
        best = max(list(graph.keys()), key=lambda x: len(graph[x]) * random() * 2)
        c += [best]
        for i in graph[best]:
            graph[i].remove(best)
            if len(graph[i]) == 0:
                del graph[i]
        del graph[best]



def eval_fitness(graph, vc):
    # get the total number of edges to cover vs. the number covered by vc
    num_edges = sum(len(graph[j]) for j in graph)
    covered_edges = {i: set() for i in range(len(vc))}
    for i, v in enumerate(vc):
        if v > 0 and i in graph:
            for j in graph[i]:
                covered_edges[i].add(j)
                covered_edges[j].add(i)
    num_covered_edges = sum(len(covered_edges[j]) for j in covered_edges)
    return num_covered_edges - num_edges - sum(vc)
