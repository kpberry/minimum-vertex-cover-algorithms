# File for the branch and bound algorithm.
# To get a lower bound, we look at the subgraph which has unassigned vertices,
# use a 2-approximation algorithm to find a solution fo that subgraph, then
# add that divided by two to the number of vertices which have already been
# assigned ones. This is implemented in the get_lower_bound function.
# To check if a configuration is a dead end, we check to see if there are any
# edges which have both endpoints assigned to 0 already. This is implemented
# in the check function.

from datetime import datetime, timedelta
from heapq import heappush, heappop, nsmallest
from random import seed

from approx import edge_deletion
from graph_utils import read_graph, remove_vertices, remove_isolates
from vc import is_solution


def get_lower_bound(graph, vc, unassigned):
    # remove all values which have been assigned 1s
    ones = [i for i in range(len(vc)) if vc[i] == 1 and not i in unassigned]
    pruned = remove_isolates(remove_vertices(graph, ones))
    # add half the result of the edge deletion approximation to the number of
    # assigned 1 vertices in the vertex cover
    result = len(ones) + sum(edge_deletion(pruned)) / 2.0
    return result


def check(graph, vc, unassigned):
    # For any edge (u, v), if both u and v are not in the vertex cover,
    # then the configuration cannot possibly be a solution, so return false
    for u in graph:
        for v in graph[u]:
            if u not in unassigned and v not in unassigned and vc[u] + vc[
                v] == 0:
                print('-----------------------failed check')
                return False
    # otherwise, return true
    return True


def branch_bound(graph, filename, cutoff_time):
    # IO stuff
    base = filename.split('/')[-1].split('.')[0] \
           + '_BnB_' + str(cutoff_time)
    with open(base + '.trace', 'w') as trace:
        start_time = cur_time = datetime.now()

        # start with a 2 approximation
        best_vc = vc = edge_deletion(graph)
        # make a list of all the unassigned vertices in the configuration, which
        # is initially all of them
        unassigned = set([i for i in range(len(best_vc)) if i in graph])
        # Compute the initial lower bound and number of vertices in the VC
        lb = get_lower_bound(graph, vc, unassigned)
        best_vc_value = vc_value = sum(best_vc)
        # Initialize the priority queue frontier as a heap and add the first
        # candidate configuration. The heap will be sorted by lower bounds.
        frontier = []
        heappush(frontier, ((lb, vc, unassigned)))

        # IO stuff; write the initial solution in case no improvements are made
        trace.write('{:0.2f}'.format(
            (cur_time - start_time).total_seconds()
        ))
        trace.write(',' + str(sum(best_vc)) + '\n')

        # Stop looping when a solution can't be improved or when time is up
        while len(frontier) > 0 and not lb == vc_value \
                and cur_time - start_time < timedelta(seconds=cutoff_time):
            # Choose step
            # get the current candidate
            lb, vc, unassigned = heappop(frontier)
            # if no changes can be made, do nothing
            if len(unassigned) == 0:
                continue

            # Expand step
            # create two children with or without the least connected vertices
            i = min(unassigned, key=lambda x: len(graph[x]))
            with_vi = [v for v in vc]
            with_vi[i] = 1
            without_vi = [v for v in vc]
            without_vi[i] = 0

            for n in [with_vi, without_vi]:
                # If the current candidate is better than the current best
                # solution, then make it the new best solution
                if is_solution(graph, n):
                    vc_value = sum(n)
                    if vc_value < best_vc_value:
                        best_vc_value = vc_value
                        best_vc = n

                        # IO stuff
                        trace.write('{:0.2f}'.format(
                            (cur_time - start_time).total_seconds()
                        ))
                        trace.write(',' + str(sum(best_vc)) + '\n')
                    else:
                        print('----------- worse solution ------------')

                # If more changes can be made, check if they should be made
                if len(unassigned) > 0:
                    # Make a copy where the vertex just assigned is no longer
                    # in the unassigned values
                    copy = set([i for i in unassigned])
                    copy.remove(i)
                    # If the candidate cannot possibly be a solution, remove it
                    if not check(graph, vc, unassigned):
                        continue
                    # If the lower bound is better than the current best value,
                    # add it to the frontier
                    lb = get_lower_bound(graph, n, unassigned)
                    if lb < best_vc_value:
                        heappush(frontier, (lb, n, copy))
                    else:
                        print('dq by lower bound--------------------')

            print(best_vc_value, lb, len(frontier))

            # Trim the frontier; get rid of any items whose lower bound after
            # an update to the solution is no longer better than that solution.
            # Helps to reduce memory usage.
            remove_start = len(frontier)
            for i in range(len(frontier)):
                if frontier[i][0] > best_vc_value:
                    remove_start = i + 1
            frontier = nsmallest(remove_start, frontier)

            cur_time = datetime.now()

    # More IO stuff.
    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(best_vc)) + '\n')
        sol.write(
            ','.join([str(i + 1) for i in range(len(best_vc)) if
                      best_vc[i] == 1]))

    return best_vc

# Run the algorithm on an input graph with a specified time and faux random seed
def run(filename, cutoff_time, random_seed=0):
    seed(random_seed)
    graph = read_graph(filename)
    return branch_bound(graph, filename, cutoff_time)
