# File containing our implementation of a variation on randomized hill climbing.
# Uses two neighbor functions: get_close_neighbor, which tries to remove a
# random vertex from a VC if doing so will keep the VC a solution, and
# get_neighbors, which removes 1 a random vertex from a graph if it is a
# solution or add 1 vertex to a graph if it is not a solution.

from datetime import datetime, timedelta
from random import random, seed, choice

from graph_utils import read_graph
from vc import is_solution, eval_fitness


def get_close_neighbor(vc, graph, iterations=5000):
    # Try 5000 times to find a close neighbor
    for i in range(iterations):
        v = int(random() * len(vc))
        if v in graph and vc[v] == 1:
            # If removing the vertex would leave an edge uncovered, then the
            # candidate vertex does not yield a close neighbor
            for u in graph[v]:
                if vc[u] == 0:
                    break
            else:
                # If there are no vertices which would break the vertex cover,
                # then we have a close neighbor.
                copy = [u for u in vc]
                copy[v] = 0
                return copy
    return None


def get_neighbors(vc, graph_is_solution, iterations=10):
    # If the vc is a solution to the graph, yield a potential neighbor with
    # a vertex potentially removed; examining one neighbor at a time is better
    # than actually producing the neighbors eagerly since a good neighbor may
    # be found in the middle or beginning of the set of candidates
    if graph_is_solution:
        for i in range(iterations):
            copy = [v for v in vc]
            # Choose a random vertex to remove (may already be removed)
            copy[int(random() * len(vc))] = 0
            yield copy
    # If the graph is not a solution, definitely add a vertex. Again, yields in
    # case early stopping is possible.
    else:
        # Get all of the vertices which could be added
        zeroes = [i for i in range(len(vc)) if vc[i] == 0]
        for i in range(iterations):
            copy = [v for v in vc]
            # Add 1 vertex
            copy[choice(zeroes)] = 1
            yield copy


def randomized_hill_climb(problem, gen_model, filename, cutoff_time,
                          random_seed):
    seed(random_seed)

    # Basic setup; construct the initial solution and evaluate its fitness
    most_fit = model = gen_model(problem)
    best_so_far = fitness = eval_fitness(problem, model)
    model_is_solution = is_solution(problem, model)

    # IO stuff
    base = filename.split('/')[-1].split('.')[0] \
           + '_LS1_' + str(cutoff_time) + '_' \
           + str(random_seed)

    with open(base + '.trace', 'w') as trace:
        start_time = cur_time = datetime.now()

        # Loop until time runs out
        while (cur_time - start_time) < timedelta(seconds=cutoff_time):
            neighbor = get_close_neighbor(model, problem)
            # If a close neighbor is found, automatically make it the candidate
            # model since it will definitely be a solution
            if neighbor is not None and model_is_solution:
                model = neighbor
                # Update the actual fitness calculation every so often; the
                # close neighbors don't use the fitness value for selection,
                # using only the actual VC size instead, so updates don't
                # matter much when VC size changes quickly. Will be
                # approximately up to date (or only slightly off) when regular
                # neighbors need the fitness to determine if they are better
                # than the best model. All this saves computation time.
                if random() > 0.99:
                    fitness = eval_fitness(problem, neighbor)
                    best_so_far = max(best_so_far, fitness)
                # Update the model if it's better than the best so far.
                if sum(neighbor) < sum(most_fit):
                    most_fit = model
                    # log results
                    trace.write('{:0.2f}'.format(
                        (cur_time - start_time).total_seconds()
                    ))
                    trace.write(',' + str(sum(most_fit)) + '\n')
            else:
                # get the model's neighbors in a random order
                neighbors = get_neighbors(model, model_is_solution)

                # update the current model if it has a neighbor with a better or
                # slightly worse fitness
                for n in neighbors:
                    fitness = eval_fitness(problem, n)
                    if fitness > best_so_far * random():
                        model = n
                        # If the current model is better than the current
                        # solution, update the solution accordingly
                        model_is_solution = is_solution(problem, model)
                        if fitness > best_so_far and model_is_solution:
                            best_so_far = fitness
                            most_fit = model
                            # log results
                            trace.write('{:0.2f}'.format(
                                (cur_time - start_time).total_seconds()
                            ))
                            trace.write(',' + str(sum(most_fit)) + '\n')
                        # Stop examining neighbors when a good one is found
                        break
            print(sum(most_fit), sum(model), fitness, best_so_far,
                  model_is_solution)

            cur_time = datetime.now()

    # More IO stuff
    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(most_fit)) + '\n')
        sol.write(','.join([str(i + 1) for i in range(len(most_fit)) if
                            most_fit[i] == 1]))
    return most_fit

# Run the algorithm on an input graph with a specified time and random seed
def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    randomized_hill_climb(graph,
                          # Generate the initial candidate as all vertices
                          lambda g: [1] * (max(graph) + 1),
                          filename, cutoff_time, random_seed)


if __name__ == '__main__':
    run('./data/Data/star.graph', 600, 0)
