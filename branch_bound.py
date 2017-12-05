from datetime import datetime, timedelta
from heapq import heappush, heappop, nsmallest
from random import seed

from approx import random_vc
from graph_utils import read_graph, remove_vertices, remove_isolates
from vc import is_solution


def get_lower_bound(graph, vc, unassigned):
    ones = [i for i in range(len(vc)) if vc[i] == 1 and not i in unassigned]
    pruned = remove_isolates(remove_vertices(graph, ones))
    result = len(ones) + sum(random_vc(pruned)) / 2.0
    return result


def check(graph, vc, unassigned):
    for u in graph:
        for v in graph[u]:
            if u not in unassigned and v not in unassigned and vc[u] + vc[
                v] == 0:
                print('-----------------------failed check')
                return False
    return True


def branch_bound(graph, filename, cutoff_time):
    base = filename.split('/')[-1].split('.')[0] \
           + '_BnB_' + str(cutoff_time)
    with open(base + '.trace', 'w') as trace:
        start_time = cur_time = datetime.now()
        # best_vc = vc = [0] * (max(graph) + 1)
        best_vc = vc = random_vc(graph)
        unassigned = set([i for i in range(len(best_vc)) if i in graph])
        lb = get_lower_bound(graph, vc, unassigned)
        best_vc_value = vc_value = sum(best_vc)
        frontier = []
        heappush(frontier, ((lb, vc, unassigned)))
        while len(frontier) > 0 and not lb == vc_value \
                and cur_time - start_time < timedelta(seconds=cutoff_time):
            lb, vc, unassigned = heappop(frontier)

            if len(unassigned) == 0:
                continue

            i = min(unassigned, key=lambda x: len(graph[x]))
            with_vi = [v for v in vc]
            with_vi[i] = 1
            without_vi = [v for v in vc]
            without_vi[i] = 0
            for n in [with_vi, without_vi]:
                if is_solution(graph, n):
                    vc_value = sum(n)
                    if vc_value < best_vc_value:
                        best_vc_value = vc_value
                        best_vc = n

                        #log change
                        trace.write('{:0.2f}'.format(
                            (cur_time - start_time).total_seconds()
                        ))
                        trace.write(',' + str(sum(best_vc)) + '\n')
                    else:
                        print('----------- worse solution ------------')

                if len(unassigned) > 0:
                    copy = set([i for i in unassigned])
                    copy.remove(i)
                    if not check(graph, vc, unassigned):
                        continue
                    lb = get_lower_bound(graph, n, unassigned)
                    if lb < best_vc_value:
                        heappush(frontier, (lb, n, copy))
                    else:
                        print('dq by lower bound--------------------')

            print(best_vc_value, lb, len(frontier))

            remove_start = len(frontier)
            for i in range(len(frontier)):
                if frontier[i][0] > best_vc_value:
                    remove_start = i + 1
            frontier = nsmallest(remove_start, frontier)

            cur_time = datetime.now()

    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(best_vc)) + '\n')
        sol.write(
            ','.join([str(i + 1) for i in range(len(best_vc)) if
                      best_vc[i] == 1]))

    return best_vc


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    return branch_bound(graph, filename, cutoff_time)


if __name__ == '__main__':
    print(sum(run('./data/Data/jazz.graph', 1000, 0)))
