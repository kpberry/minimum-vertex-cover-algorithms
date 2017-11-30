from collections import deque
from math import inf
from queue import PriorityQueue
from random import choice

# import cvxopt
import pulp as lp

from approx import random_vc
from graph_utils import read_graph, remove_vertices, remove_isolates, get_edges
from vc import is_solution, construct_vc


def get_lower_bound(graph, vc, assigned):
    ones = [i for i in assigned if vc[i] == 1]
    pruned = remove_isolates(remove_vertices(graph, ones))

    # edges = get_edges(pruned)
    #
    # problem = lp.LpProblem('VC', lp.LpMinimize)
    # x = lp.LpVariable.dict('x', list(graph.keys()), lowBound=0)
    # problem += sum(x[i] for i in x)
    # for e in edges:
    #     problem += (x[e[0]] + x[e[1]] >= 1)
    #
    # problem.solve()
    # result = sum([lp.value(x[i]) for i in x]) + len(ones)

    # objective = cvxopt.matrix([1.0] * len(vc))
    # lhs = cvxopt.matrix(
    #     [[-1.0 if u in graph and v in graph[u] and u < v else 0.0 for v in range(len(vc))]
    #      for u in range(len(vc))])
    # rhs = cvxopt.matrix([-1.0] * len(vc))
    # print(lhs)
    # print(rhs)
    # print(objective)
    # result = sum(cvxopt.solvers.lp(objective, lhs, rhs))

    result = len(ones) + len(construct_vc(pruned)) / 2
    #
    # if len(pruned) > 0:
    #     result = len(ones) + sum(random_vc(pruned)) / 2
    # else:
    #     result = len(ones)

    return result


def branch_bound(graph, filename, cutoff_time, get_lower_bound=get_lower_bound):
    best_vc = cur_vc = [1] * (max(graph) + 1)
    # best_vc = cur_vc = construct_vc(graph)
    best_vc_value = inf
    frontier = PriorityQueue()
    frontier.put((sum(best_vc), cur_vc, set([i for i in range(len(best_vc))])))
    while not frontier.empty():
        lb, vc, unassigned = frontier.get()

        print(best_vc_value, lb, frontier.qsize())
        if lb < best_vc_value and is_solution(graph, vc):
            vc_value = sum(vc)
            if vc_value < best_vc_value:
                best_vc_value = vc_value
                best_vc = vc
            # # maybe this shouldn't be an else?
            if len(unassigned) > 0:
                i = list(unassigned)[0] # get most connected instead
                with_vi = [v for v in vc]
                with_vi[i] = 1
                without_vi = [v for v in vc]
                without_vi[i] = 0
                nexts = [with_vi, without_vi]
                for n in nexts:
                    copy = set([i for i in unassigned])
                    copy.remove(i)
                    assigned = set([i for i in range(len(vc))]) - copy
                    lb = get_lower_bound(graph, n, assigned)
                    if lb <= best_vc_value:
                        frontier.put((lb, n, copy))
    return best_vc


def run(filename, cutoff_time):
    graph = read_graph(filename)
    branch_bound(graph, filename, cutoff_time)


if __name__ == '__main__':
    run('./data/Data/email.graph', 100000)
